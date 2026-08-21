import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'redditClone.settings')
django.setup()

from subreddits.models import Subreddit
from posts.models import Post, Comment
from users.models import CustomUser

print("Seeding Mithila Communities, Posts, and Comments...")

# Get or create admin user
user, created = CustomUser.objects.get_or_create(
    username='abhishekmishra',
    defaults={
        'email': 'abhishek@mithilamilan.com',
        'is_staff': True,
        'is_superuser': True
    }
)
if created:
    user.set_password('mithila123')
    user.save()

# Sample users for community engagement
users_data = ['ramesh_jha', 'sunita_thakur', 'mithila_scholar', 'priya_chowdhury']
created_users = [user]
for u_name in users_data:
    u, _ = CustomUser.objects.get_or_create(
        username=u_name,
        defaults={'email': f'{u_name}@mithilamilan.com'}
    )
    created_users.append(u)

# Seed Subreddits
subreddits_data = [
    {
        'name': 'Madhubani',
        'description': 'मधुबनी जिलाक गप-शप, कला, संस्कृति आ स्थानीय समाचार।',
        'rules': '1. परस्पर आदर राखू।\n2. मिथिला संस्कृति आ कलाक सम्मान करू।'
    },
    {
        'name': 'Darbhanga',
        'description': 'दरभंगा शहर, राज परिसर, एलएनएमयू आ सांस्कृतिक अपडेट।',
        'rules': '1. भाषाक मर्यादा राखू।\n2. भ्रामक समाचार नहि शेयर करू।'
    },
    {
        'name': 'Samastipur',
        'description': 'समस्तीपुर जिला आ आसपासक क्षेत्रक सामुदायिक संवाद।',
        'rules': '1. सभक विचार का स्वागत अछि।'
    },
    {
        'name': 'Sitamarhi',
        'description': 'पुनौरा धाम आ सीतामढ़ी क्षेत्रक पावन गप-शप।',
        'rules': '1. सांस्कृतिक गरिमा बनाब राखू।'
    },
    {
        'name': 'Maithili',
        'description': 'मैथिली भाषा, साहित्य, कविता आ गद्य संवाद।',
        'rules': '1. मैथिली भाषा एवं साहित्यक संवर्धन।'
    },
    {
        'name': 'Mithila Food',
        'description': 'दही-चूड़ा, मखान, तिलकुट, माछ आ मिथिलाक पारंपरिक भोजन।',
        'rules': '1. स्वादिष्ट रेसिपी आ भोजनक चर्चा।'
    },
    {
        'name': 'Mithila Culture',
        'description': 'मिथिला चित्रकला, पाग, अरिपण आ पारंपरिक रीति-रिवाज।',
        'rules': '1. धरोहर आ कला संरक्षण।'
    },
]

sub_objects = {}
for sub_info in subreddits_data:
    sub, _ = Subreddit.objects.get_or_create(
        name=sub_info['name'],
        defaults={
            'description': sub_info['description'],
            'rules': sub_info['rules'],
            'creator': user,
            'approval_status': 'approved'
        }
    )
    sub.approval_status = 'approved'
    sub.save()
    sub_objects[sub.name] = sub

# Seed Sample Posts
posts_data = [
    {
        'subreddit': sub_objects['Madhubani'],
        'title': 'मधुबनी चित्रकलाक वैश्विक पहचान आ नए युवा कलाकारों का योगदान',
        'content': 'मिथिलाक जितवारपुर आ रांटी गामक चित्रकला आब पूरे विश्व में प्रसिद्ध अछि। नए पीढ़ीक कलाकार आब डिजिटल माध्यम से सेहो अपन कला के दुनिया के देखा रहल छथि। अहाँक पसंदीदा मधुबनी पेंटिंग शैली कोन अछि? भरनी, कचनी, या तांत्रिक शैली?',
        'author': created_users[1],
        'score': 24,
    },
    {
        'subreddit': sub_objects['Darbhanga'],
        'title': 'दरभंगा राज परिसर आ प्रसिद्ध श्यामा माई मंदिर प्रांगणक सौंदर्य',
        'content': 'दरभंगा राज परिसर स्थित श्यामा माई मंदिर मिथिलाक अनुपम धरोहर अछि। नवरात्र आ दुर्गा पूजा के समय एतए दीप प्रकाश आ संध्या आरती देखबाक दृश्य भव्य होइत अछि। जे सेहो दर्शन लेल आबैत छथि, ओ अलौकिक शांति महसूस करैत छथि।',
        'author': created_users[2],
        'score': 38,
    },
    {
        'subreddit': sub_objects['Mithila Food'],
        'title': 'मिथिलाक प्रामाणिक मखान आ दही-चूड़ा भोज परंपरा',
        'content': 'कोनो सेहो पावनि-तिहार हो, मिथिला में मखान, दही-चूड़ा आ तिलकुटक मिठास के बिना उत्सव अधूरा मानल जाइत अछि। जीआई टैग भेल मखान आब देश-विदेश में स्वास्थ्यवर्धक सुपरफूड मानल जा रहल अछि।',
        'author': created_users[3],
        'score': 19,
    },
    {
        'subreddit': sub_objects['Maithili'],
        'title': 'महाकवि विद्यापतिक पदावली आ आधुनिक मैथिली कविता संग्रह',
        'content': 'महाकवि विद्यापतिक शृंगार आ भक्ति रसक पद आजुओ मिथिलाक हर घर में गाओल जाइत अछि। "उगलना मोरा महादेव" सं लके "नव वृंदावन" धरि, विद्यापतिक वाणी अमर अछि।',
        'author': created_users[4],
        'score': 42,
    },
]

for p_data in posts_data:
    p, created = Post.objects.get_or_create(
        title=p_data['title'],
        defaults={
            'subreddit': p_data['subreddit'],
            'content': p_data['content'],
            'author': p_data['author'],
            'post_type': 'text',
            'score': p_data['score']
        }
    )
    if created:
        p.upvotes.add(user)
        p.upvotes.add(created_users[1])
        p.update_score()

        # Add top-level comment
        c1 = Comment.objects.create(
            post=p,
            author=created_users[2],
            content='जय मिथिला! बहुत नीक जानकारी साझा केलियैक।'
        )
        # Add reply to c1
        c2 = Comment.objects.create(
            post=p,
            author=created_users[3],
            parent=c1,
            content='सही कहलियैक, मिथिलाक कला आ संस्कृति अद्वितीय अछि।'
        )
        # Add sub-reply to c2
        Comment.objects.create(
            post=p,
            author=user,
            parent=c2,
            content='अहाँ सभक विचार सँ MithilaMilan मंच और समृद्ध भऽ रहल अछि!'
        )

print("Mithila seeding successfully completed!")
