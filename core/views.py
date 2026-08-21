from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from posts.models import Post
from subreddits.models import Subreddit
from pg_rental.models import PGListing
from job_portal.models import Job
from news.models import News
from coupon_service.models import Coupon
from storytelling.models import Story
from lost_and_found.models import LostAndFoundItem
from datetime import date
from mithila_panchang.models import MithilaSong, PanchangDay, Festival

def home(request):
    posts = Post.objects.all().order_by('-created_at')[:20]
    subreddits = Subreddit.objects.filter(approval_status='approved').order_by('-created_at')[:6]
    featured_pgs = PGListing.objects.filter(is_active=True, approval_status='Approved').order_by('-created_at')[:4]
    featured_jobs = Job.objects.filter(status='APPROVED', is_filled=False).order_by('-created_at')[:4]
    latest_news = News.objects.filter(is_published=True).order_by('-created_at')[:4]
    active_coupons = Coupon.objects.filter(is_active=True).order_by('-created_at')[:4]
    recent_stories = Story.objects.filter(status='APPROVED').order_by('-created_at')[:4]
    lost_found_items = LostAndFoundItem.objects.filter(status='APPROVED', is_resolved=False).order_by('-created_at')[:4]
    mithila_songs = MithilaSong.objects.filter(is_published=True).order_by('order')[:6]
    
    # Panchang Today & Upcoming Festival Data
    today = date.today()
    HINDI_MONTHS = {
        1: 'जनवरी', 2: 'फरवरी', 3: 'मार्च', 4: 'अप्रैल', 5: 'मई', 6: 'जून',
        7: 'जुलाई', 8: 'अगस्त', 9: 'सितंबर', 10: 'अक्टूबर', 11: 'नवंबर', 12: 'दिसंबर'
    }
    today_date_hi = f"{today.day} {HINDI_MONTHS.get(today.month, '')}"

    today_panchang = PanchangDay.objects.filter(date=today).first()
    if not today_panchang:
        today_panchang = PanchangDay.objects.filter(date__lte=today).order_by('-date').first()
        if not today_panchang:
            today_panchang = PanchangDay.objects.order_by('date').first()

    upcoming_festival = Festival.objects.filter(date__gte=today).order_by('date').first()
    if not upcoming_festival:
        upcoming_festival = Festival.objects.order_by('date').first()

    upcoming_festival_date_hi = ""
    if upcoming_festival:
        upcoming_festival_date_hi = f"{upcoming_festival.date.day} {HINDI_MONTHS.get(upcoming_festival.date.month, '')}"

    context = {
        'posts': posts,
        'subreddits': subreddits,
        'featured_pgs': featured_pgs,
        'featured_jobs': featured_jobs,
        'latest_news': latest_news,
        'active_coupons': active_coupons,
        'recent_stories': recent_stories,
        'lost_found_items': lost_found_items,
        'mithila_songs': mithila_songs,
        'today_panchang': today_panchang,
        'upcoming_festival': upcoming_festival,
        'today_date': today,
        'today_date_hi': today_date_hi,
        'upcoming_festival_date_hi': upcoming_festival_date_hi,
    }
    
    return render(request, 'core/home.html', context)

def set_location(request):
    if request.method == 'POST':
        city_slug = request.POST.get('city_slug')
        next_url = request.POST.get('next', request.META.get('HTTP_REFERER', '/'))
        
        if city_slug == 'all' or not city_slug:
            request.session['active_city_slug'] = None
            if request.user.is_authenticated:
                UserLocationPreference.objects.filter(user=request.user).update(city=None)
            messages.info(request, "Location set to All India")
        else:
            try:
                city = City.objects.get(slug=city_slug)
                request.session['active_city_slug'] = city.slug
                if request.user.is_authenticated:
                    pref, created = UserLocationPreference.objects.get_or_create(user=request.user)
                    pref.city = city
                    pref.save()
                messages.success(request, f"Location updated to {city.name}")
            except City.DoesNotExist:
                messages.error(request, "Selected city not found.")
                
        return redirect(next_url)
    return redirect('core:home')

from .models import LegalPage, FooterSetting

def about(request):
    return render(request, 'core/about.html')

def _get_or_create_legal_page(slug, title, summary, default_html):
    page = LegalPage.objects.filter(slug=slug, is_active=True).first()
    if not page:
        page = LegalPage.objects.create(
            slug=slug,
            title=title,
            summary=summary,
            content=default_html
        )
    elif len(page.content.strip()) < 100:
        page.content = default_html
        page.summary = summary
        page.save()
    return page

def terms(request):
    default_content = """
    <h3>1. Introduction & Acceptance of Terms</h3>
    <p>Welcome to <strong>MithilaMilan</strong> ("Platform", "we", "us", or "our"). MithilaMilan is a community and information platform dedicated to connecting people, culture, businesses, stories, opportunities, and information related to Mithila.</p>
    <p>By accessing, browsing, registering for, or using MithilaMilan, you agree to be bound by these Terms of Service ("Terms"). If you do not agree with any part of these Terms, you must immediately discontinue using the platform.</p>
    
    <h3>2. User Eligibility & Account Registration</h3>
    <p>You must be at least 18 years old or the legal age of majority in your jurisdiction to create an account. When creating an account, you agree to provide accurate, complete, and updated information. You are solely responsible for maintaining the confidentiality of your account credentials (password, OTP, PIN) and for all activities that occur under your account.</p>

    <h3>3. Platform Status & Third-Party Content Disclaimer</h3>
    <div class="legal-callout warning">
        <strong>Important Notice:</strong> MithilaMilan is a community and information platform. Content, listings, advertisements, products, services, events, jobs, rentals, matrimonial profiles, and other information are submitted or provided by users, independent businesses, organizers, or third parties. MithilaMilan does not automatically endorse, verify, or guarantee every third-party listing, product quality, or user claim.
    </div>
    <p>MithilaMilan is not responsible for fraudulent, misleading, unauthorized, or unlawful activities carried out by third parties through information, listings, posts, advertisements, transactions, or communications on the platform, subject to applicable law.</p>
    <p><strong>User Verification Obligation:</strong> Users are solely responsible for verifying information, identities, background checks, offers, prices, payment details, property condition, job authenticity, and other claims before entering into any financial transaction, rental agreement, or contract.</p>

    <h3>4. User-Generated Content & Ownership</h3>
    <p>User-generated content belongs to its respective authors. By posting content on MithilaMilan (including posts, comments, stories, listings, photos, or reviews), you grant MithilaMilan a worldwide, non-exclusive, royalty-free license to host, display, reproduce, and distribute your content across the platform.</p>
    <p>You represent and warrant that you own or have necessary rights to all content you submit and that your content does not violate copyright, trademark, privacy, or legal rights of any third party.</p>

    <h3>5. Prohibited Activities</h3>
    <ul>
        <li>Posting false, fraudulent, deceptive, or misleading listings or services.</li>
        <li>Impersonating any person, business, or organization.</li>
        <li>Harassing, abusing, threatening, or defaming other users.</li>
        <li>Sharing sensitive financial or personal data (passwords, OTPs, bank credentials).</li>
        <li>Spamming, posting unauthorized advertising, or distributing malware.</li>
        <li>Attempting to reverse engineer or breach the platform's security.</li>
    </ul>

    <h3>6. Content Moderation & Account Termination</h3>
    <p>MithilaMilan reserves the right to review, moderate, restrict, edit, reject, or remove any content or listing that violates applicable laws, platform policies, or community guidelines. We reserve the right to suspend or terminate accounts that engage in repeated or severe policy violations without prior notice.</p>

    <h3>7. Limitation of Liability</h3>
    <p>To the maximum extent permitted by law, MithilaMilan, its founders, team, and affiliates shall not be liable for any indirect, incidental, special, consequential, or punitive damages arising out of your access to, use of, or inability to use the platform or any third-party transactions conducted through the platform.</p>

    <h3>8. Contact Us</h3>
    <p>If you have questions or concerns regarding these Terms, please contact us at <a href="mailto:support@mithilamilan.com">support@mithilamilan.com</a>.</p>
    """
    page = _get_or_create_legal_page('terms', 'Terms of Service', 'Standard terms governing the access and use of the MithilaMilan community platform.', default_content)
    return render(request, 'core/legal_page.html', {'page': page})

def privacy(request):
    default_content = """
    <h3>1. Information We Collect</h3>
    <p>MithilaMilan respects your privacy. We collect information you provide directly to us (e.g., account details, name, email address, location preferences, posts, listings, profile information) and automated data (e.g., IP address, device type, browser information, pages visited).</p>

    <h3>2. How We Use Your Information</h3>
    <ul>
        <li>To provide, maintain, and improve platform functionality.</li>
        <li>To personalize content, local feeds, and community experiences.</li>
        <li>To communicate notifications, support responses, and platform updates.</li>
        <li>To detect, prevent, and respond to fraud, unauthorized activity, or security issues.</li>
    </ul>

    <h3>3. Data Sharing & Disclosure</h3>
    <p>We do not sell your personal data to third parties. Information may be shared with service providers under strict data protection terms, or as required by law, legal process, or law enforcement requests.</p>
    <div class="legal-callout info">
        <strong>Public Profiles & Listings:</strong> Information you explicitly choose to publish publicly (e.g. username, public posts, store items, job listings, matrimonial profiles, PG listings) will be visible to other platform users.
    </div>

    <h3>4. Data Security</h3>
    <p>We employ administrative, technical, and physical safeguards designed to protect personal information from unauthorized access, alteration, or disclosure. However, no internet transmission is 100% secure.</p>

    <h3>5. Cookies & Tracking</h3>
    <p>MithilaMilan uses cookies and local storage to store session preferences (such as selected city/locality) and authentication tokens for a seamless user experience.</p>

    <h3>6. Your Rights</h3>
    <p>You have the right to access, update, or request deletion of your personal account data by visiting your profile settings or contacting <a href="mailto:privacy@mithilamilan.com">privacy@mithilamilan.com</a>.</p>
    """
    page = _get_or_create_legal_page('privacy', 'Privacy Policy', 'Details on how MithilaMilan collects, uses, protects, and handles your personal data.', default_content)
    return render(request, 'core/legal_page.html', {'page': page})

def cancellation(request):
    default_content = """
    <h3>1. Order & Subscription Cancellations</h3>
    <p>This Cancellation Policy applies to orders placed on <strong>Mithila Store</strong>, event tickets registered through MithilaMilan, or paid premium listings/subscriptions on the platform.</p>

    <h3>2. Customer-Initiated Cancellations</h3>
    <ul>
        <li><strong>Physical Products (Mithila Store):</strong> You may cancel a product order before it has been dispatched by the seller. Once an item is shipped, cancellation requests cannot be processed directly; instead, follow the <a href="/refund-policy/">Refund & Return Policy</a>.</li>
        <li><strong>Event Registrations & Services:</strong> Event registration cancellations depend on the specific organizer's policy stated on the event detail page.</li>
        <li><strong>Digital / Subscriptions / Classified Listings:</strong> Listing fees or digital promotional packages are non-cancellable once the listing has gone live.</li>
    </ul>

    <h3>3. Seller / Platform-Initiated Cancellations</h3>
    <p>Mithila Milan or independent sellers reserve the right to cancel any order or booking under circumstances including but not limited to:</p>
    <ul>
        <li>Unavailability of item stock or event venue cancellation.</li>
        <li>Inaccurate product details or pricing errors.</li>
        <li>Fraudulent transaction detection or failure of payment verification.</li>
    </ul>
    <p>In case of seller or platform-initiated cancellations, a full refund will be credited to the original payment method.</p>
    """
    page = _get_or_create_legal_page('cancellation', 'Cancellation Policy', 'Policy governing order, service, and listing cancellations on MithilaMilan.', default_content)
    return render(request, 'core/legal_page.html', {'page': page})

def community_guidelines(request):
    default_content = """
    <h3>1. Our Vision for MithilaMilan Community</h3>
    <p>MithilaMilan aims to be a vibrant, respectful, and safe digital space for the people of Mithila worldwide to connect, share culture, exchange ideas, and support local initiatives.</p>

    <h3>2. Core Principles</h3>
    <ul>
        <li><strong>Respect & Inclusivity:</strong> Treat fellow community members with dignity. Hate speech, discrimination, harassment, or personal attacks will not be tolerated.</li>
        <li><strong>Authenticity:</strong> Share authentic stories, genuine opportunities, and verified listings. Do not create deceptive profiles or spread misinformation.</li>
        <li><strong>Cultural Heritage:</strong> Honor and promote Maithili culture, art, language, literature, and tradition constructively.</li>
    </ul>

    <h3>3. Prohibited Content</h3>
    <div class="legal-callout warning">
        <strong>Zero Tolerance Items:</strong> Explicit adult content, violence, hate speech targeting caste/religion/gender, abusive harassment, illegal trade, and financial scams are strictly prohibited.
    </div>

    <h3>4. Reporting Violations</h3>
    <p>If you encounter content or behavior violating these guidelines, use the <strong>Report</strong> button on the post/listing or contact <a href="/report-issue/">Report an Issue</a>.</p>
    """
    page = _get_or_create_legal_page('community-guidelines', 'Community Guidelines', 'Standards and guidelines for respectful interaction across MithilaMilan communities.', default_content)
    return render(request, 'core/legal_page.html', {'page': page})

def content_policy(request):
    default_content = """
    <h3>1. Scope of Content Policy</h3>
    <p>This Content Policy governs all user-submitted text, photos, audio, video, listings, store items, and comments across MithilaMilan.</p>

    <h3>2. Ownership & Responsibility</h3>
    <p>User-generated content belongs to its respective authors. Users are solely responsible for the legality, accuracy, and appropriateness of the content they submit. MithilaMilan does not pre-screen all content but reserves full moderation rights.</p>

    <h3>3. Copyright & Intellectual Property</h3>
    <p>Respect intellectual property. Do not post copyrighted artwork, photos, books, or trademarked material without authorization. Infringing content will be removed upon receiving a valid DMCA/takedown request at <a href="mailto:copyright@mithilamilan.com">copyright@mithilamilan.com</a>.</p>

    <h3>4. Content Moderation & Removal</h3>
    <p>MithilaMilan may review, moderate, edit, restrict, or remove content that violates applicable laws, copyright, safety regulations, or platform guidelines.</p>
    """
    page = _get_or_create_legal_page('content-policy', 'Content Policy', 'Rules regarding content creation, copyright, user ownership, and moderation.', default_content)
    return render(request, 'core/legal_page.html', {'page': page})

def refund_policy(request):
    default_content = """
    <h3>1. Refund & Return Eligibility</h3>
    <p>Products purchased from independent sellers on <strong>Mithila Store</strong> are subject to seller-specific return terms displayed on the product page.</p>

    <h3>2. General Return Conditions</h3>
    <ul>
        <li>Defective, damaged, or incorrect items received must be reported within 48 hours of delivery with photo evidence.</li>
        <li>Handicraft and Madhubani art items are unique handcrafted creations; slight natural variations in color/texture are not considered defects.</li>
        <li>Customized or made-to-order products are non-returnable unless defective.</li>
    </ul>

    <h3>3. Refund Processing</h3>
    <p>Approved refunds will be processed back to the original payment method within 5-7 business days of seller inspection and approval.</p>

    <h3>4. Marketplace Disclaimer</h3>
    <div class="legal-callout info">
        Products and services listed by independent sellers or providers are subject to separate seller terms, availability, delivery, and return conditions. Users should review product terms before completing purchase.
    </div>
    """
    page = _get_or_create_legal_page('refund-policy', 'Refund Policy', 'Details on returns, exchanges, and refund processing for marketplace purchases.', default_content)
    return render(request, 'core/legal_page.html', {'page': page})

def disclaimer(request):
    default_content = """
    <h3>1. General Platform Disclaimer</h3>
    <div class="legal-callout warning">
        <strong>Important:</strong> MithilaMilan is a community and information platform. Content, listings, advertisements, products, services, events, jobs, rentals, matrimonial profiles, and other information may be submitted or provided by users, businesses, organizers, or third parties. MithilaMilan does not automatically endorse or guarantee every third-party listing or claim.
    </div>

    <h3>2. Third-Party Liability Disclaimer</h3>
    <p>MithilaMilan is not responsible for fraudulent, misleading, unauthorized, or unlawful activities carried out by third parties through information, listings, posts, advertisements, transactions, or communications on the platform, subject to applicable law.</p>

    <h3>3. User Verification Duty</h3>
    <p>Users are responsible for verifying information, identities, offers, prices, payment details, property physical conditions, job credentials, and other claims before entering into any transaction, agreement, or financial commitment.</p>

    <h3>4. Marketplace Disclaimer</h3>
    <p>Products and services listed by independent sellers or providers may be subject to separate seller terms, availability, pricing, delivery, and return conditions. Users should review applicable details before purchasing.</p>

    <h3>5. Fraud & Scam Safety Warning</h3>
    <div class="legal-callout danger">
        <strong>⚠️ Stay Safe:</strong> Never share your OTP, password, PIN, card details, or other sensitive information with anyone claiming to represent MithilaMilan. MithilaMilan will never ask you to transfer money to a personal account for verification or account activation.
    </div>
    """
    page = _get_or_create_legal_page('disclaimer', 'Disclaimer', 'Important platform disclaimers, user verification duties, and liability notices.', default_content)
    return render(request, 'core/legal_page.html', {'page': page})

def contact(request):
    footer_settings = FooterSetting.objects.first()
    return render(request, 'core/contact.html', {'footer_settings': footer_settings})

def report_issue(request):
    footer_settings = FooterSetting.objects.first()
    return render(request, 'core/report_issue.html', {'footer_settings': footer_settings})