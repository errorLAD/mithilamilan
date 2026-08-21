/**
 * MithilaMilan Global Persistent Audio Controller
 * Synchronizes single global audio player across Turbo SPA navigation & localStorage.
 */
(function() {
    const STORAGE_KEY = 'mithilamilan_audio_state';

    const defaultState = {
        songId: 'H501incNC74',
        title: 'मिथिलाक पावन लोकगीत',
        singer: 'मैथिली सुर संगीत',
        cover: 'https://img.youtube.com/vi/H501incNC74/hqdefault.jpg',
        audioUrl: '',
        currentTime: 0,
        duration: 0,
        volume: 80,
        isMuted: false,
        isPlaying: false,
        expanded: false
    };

    window.MithilaAudio = {
        state: { ...defaultState },
        ytPlayer: null,
        html5Audio: null,
        timerId: null,
        isYtReady: false,
        playerType: 'yt', // 'yt' or 'html5'

        init() {
            this.loadState();
            this.setupHtml5Audio();
            this.loadYtApi();
            this.setupEventListeners();
            this.startSaveTimer();
        },

        loadState() {
            try {
                const saved = localStorage.getItem(STORAGE_KEY);
                if (saved) {
                    const parsed = JSON.parse(saved);
                    // Retain saved currentTime, volume, song details
                    this.state = { ...defaultState, ...parsed };
                }
            } catch (e) {
                console.error('Error loading audio state:', e);
            }
        },

        saveState() {
            try {
                localStorage.setItem(STORAGE_KEY, JSON.stringify({
                    songId: this.state.songId,
                    title: this.state.title,
                    singer: this.state.singer,
                    cover: this.state.cover,
                    audioUrl: this.state.audioUrl,
                    currentTime: this.state.currentTime || 0,
                    duration: this.state.duration || 0,
                    volume: this.state.volume || 80,
                    isMuted: this.state.isMuted || false,
                    isPlaying: this.state.isPlaying || false
                }));
            } catch (e) {
                console.error('Error saving audio state:', e);
            }
        },

        setupHtml5Audio() {
            let el = document.getElementById('global-html5-audio');
            if (!el) {
                el = document.createElement('audio');
                el.id = 'global-html5-audio';
                el.style.display = 'none';
                document.body.appendChild(el);
            }
            this.html5Audio = el;

            el.addEventListener('timeupdate', () => {
                if (this.playerType === 'html5') {
                    this.state.currentTime = el.currentTime;
                    this.state.duration = el.duration || 0;
                    this.notifyUI();
                }
            });

            el.addEventListener('ended', () => {
                if (this.playerType === 'html5') {
                    this.state.isPlaying = false;
                    this.notifyUI();
                    this.saveState();
                }
            });
        },

        loadYtApi() {
            if (window.YT && window.YT.Player) {
                this.initYtPlayer();
            } else {
                const prev = window.onYouTubeIframeAPIReady;
                window.onYouTubeIframeAPIReady = () => {
                    if (prev) prev();
                    this.initYtPlayer();
                };
            }
        },

        initYtPlayer() {
            if (this.ytPlayer) return;
            const container = document.getElementById('global-yt-iframe');
            if (!container) return;

            this.ytPlayer = new YT.Player('global-yt-iframe', {
                height: '100%',
                width: '100%',
                videoId: this.state.songId || 'H501incNC74',
                playerVars: {
                    'playsinline': 1,
                    'autoplay': 0,
                    'controls': 0,
                    'rel': 0,
                    'modestbranding': 1
                },
                events: {
                    'onReady': () => {
                        this.isYtReady = true;
                        if (this.state.volume) {
                            this.ytPlayer.setVolume(this.state.volume);
                        }
                        if (this.state.currentTime > 0) {
                            this.ytPlayer.seekTo(this.state.currentTime, true);
                        }
                    },
                    'onStateChange': (e) => {
                        if (e.data === YT.PlayerState.PLAYING) {
                            this.state.isPlaying = true;
                            this.state.duration = this.ytPlayer.getDuration() || 0;
                            this.notifyUI();
                        } else if (e.data === YT.PlayerState.PAUSED) {
                            this.state.isPlaying = false;
                            this.notifyUI();
                        } else if (e.data === YT.PlayerState.ENDED) {
                            this.state.isPlaying = false;
                            this.notifyUI();
                        }
                    }
                }
            });
        },

        startSaveTimer() {
            if (this.timerId) clearInterval(this.timerId);
            this.timerId = setInterval(() => {
                if (this.state.isPlaying) {
                    if (this.playerType === 'yt' && this.ytPlayer && this.ytPlayer.getCurrentTime) {
                        const cur = this.ytPlayer.getCurrentTime();
                        if (cur && cur > 0) {
                            this.state.currentTime = cur;
                        }
                        this.state.duration = this.ytPlayer.getDuration() || 0;
                    }
                    this.saveState();
                    this.notifyUI();
                }
            }, 1000);
        },

        playSong(song) {
            if (!song) return;

            const isSame = (song.id && song.id === this.state.songId) || (song.audio_url && song.audio_url === this.state.audioUrl);

            if (isSame) {
                this.togglePlay();
                return;
            }

            // New Song
            this.state.songId = song.id || '';
            this.state.title = song.title || 'मैथिली गीत';
            this.state.singer = song.singer || 'मैथिली कलाकार';
            this.state.cover = song.cover || (song.id ? `https://img.youtube.com/vi/${song.id}/hqdefault.jpg` : '');
            this.state.audioUrl = song.audio_url || '';
            this.state.currentTime = 0;
            this.state.isPlaying = true;

            if (song.audio_url) {
                this.playerType = 'html5';
                if (this.ytPlayer && this.ytPlayer.pauseVideo) this.ytPlayer.pauseVideo();
                this.html5Audio.src = song.audio_url;
                this.html5Audio.volume = this.state.volume / 100;
                this.html5Audio.play().catch(console.error);
            } else if (song.id) {
                this.playerType = 'yt';
                if (this.html5Audio) this.html5Audio.pause();
                if (this.ytPlayer && this.ytPlayer.loadVideoById) {
                    this.ytPlayer.loadVideoById(song.id, 0);
                    this.ytPlayer.playVideo();
                }
            }

            this.saveState();
            this.notifyUI();
        },

        pause() {
            this.state.isPlaying = false;
            if (this.playerType === 'yt' && this.ytPlayer && this.ytPlayer.pauseVideo) {
                this.ytPlayer.pauseVideo();
            } else if (this.playerType === 'html5' && this.html5Audio) {
                this.html5Audio.pause();
            }
            this.saveState();
            this.notifyUI();
        },

        resume() {
            this.state.isPlaying = true;
            if (this.playerType === 'yt' && this.ytPlayer && this.ytPlayer.playVideo) {
                this.ytPlayer.playVideo();
            } else if (this.playerType === 'html5' && this.html5Audio) {
                this.html5Audio.play().catch(console.error);
            }
            this.saveState();
            this.notifyUI();
        },

        togglePlay() {
            if (this.state.isPlaying) {
                this.pause();
            } else {
                this.resume();
            }
        },

        seekTo(seconds) {
            this.state.currentTime = seconds;
            if (this.playerType === 'yt' && this.ytPlayer && this.ytPlayer.seekTo) {
                this.ytPlayer.seekTo(seconds, true);
            } else if (this.playerType === 'html5' && this.html5Audio) {
                this.html5Audio.currentTime = seconds;
            }
            this.saveState();
            this.notifyUI();
        },

        setVolume(percent) {
            this.state.volume = percent;
            if (this.ytPlayer && this.ytPlayer.setVolume) {
                this.ytPlayer.setVolume(percent);
            }
            if (this.html5Audio) {
                this.html5Audio.volume = percent / 100;
            }
            this.saveState();
            this.notifyUI();
        },

        formatTime(sec) {
            if (!sec || isNaN(sec)) return '00:00';
            const m = Math.floor(sec / 60);
            const s = Math.floor(sec % 60);
            return `${m < 10 ? '0' : ''}${m}:${s < 10 ? '0' : ''}${s}`;
        },

        notifyUI() {
            window.dispatchEvent(new CustomEvent('mithila-audio-update', { detail: this.state }));
        },

        setupEventListeners() {
            // Turbo page navigation handling: Prevent Turbo from re-creating or detaching the audio player DOM element
            document.addEventListener('turbo:before-render', (e) => {
                const existingPlayer = document.getElementById('global-music-player');
                const newPlayer = e.detail.newBody.querySelector('#global-music-player');
                if (existingPlayer && newPlayer) {
                    newPlayer.replaceWith(existingPlayer);
                }
            });

            window.addEventListener('beforeunload', () => {
                if (this.playerType === 'yt' && this.ytPlayer && this.ytPlayer.getCurrentTime) {
                    const cur = this.ytPlayer.getCurrentTime();
                    if (cur && cur > 0) {
                        this.state.currentTime = cur;
                    }
                }
                this.saveState();
            });
        }
    };

    window.playGlobalSong = function(id, title, singer, cover, audioUrl) {
        let songObj = {};
        if (typeof id === 'object') {
            songObj = id;
        } else {
            songObj = { id, title, singer, cover, audio_url: audioUrl };
        }
        window.MithilaAudio.playSong(songObj);
    };

    document.addEventListener('DOMContentLoaded', () => {
        window.MithilaAudio.init();
    });
})();
