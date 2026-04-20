import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_HOST = "mail.octava.my.id"
SMTP_PORT = 587
SMTP_USER = "bayumili@octava.my.id"
SMTP_PASSWORD = "2shot@Caffelatte"
SMTP_FROM = "bayumili@octava.my.id"

to = "qoisoctava20@gmail.com"
subject = "🔥 Limited Time Offer – Don't Miss Out!"

html = """
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body { margin: 0; padding: 0; background: #f0f0f0; font-family: Arial, sans-serif; }
    .wrapper { max-width: 600px; margin: 30px auto; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,0.1); }
    .hero { background: linear-gradient(135deg, #FF6B35, #F7C59F); padding: 50px 40px; text-align: center; }
    .hero h1 { margin: 0 0 8px; font-size: 36px; color: #fff; text-shadow: 0 2px 4px rgba(0,0,0,0.2); }
    .hero p { margin: 0; font-size: 16px; color: #fff3ec; }
    .badge { display: inline-block; background: #fff; color: #FF6B35; font-weight: bold; font-size: 13px; padding: 6px 16px; border-radius: 20px; margin-top: 16px; letter-spacing: 1px; }
    .body { padding: 36px 40px; }
    .body h2 { margin: 0 0 12px; font-size: 22px; color: #222; }
    .body p { color: #555; line-height: 1.7; font-size: 15px; }
    .features { display: table; width: 100%; margin: 24px 0; }
    .feature { display: table-cell; width: 33%; text-align: center; padding: 16px 10px; }
    .feature .icon { font-size: 28px; }
    .feature .label { font-size: 13px; color: #444; margin-top: 6px; font-weight: bold; }
    .cta { text-align: center; margin: 30px 0 10px; }
    .cta a { background: #FF6B35; color: #fff; text-decoration: none; padding: 16px 48px; border-radius: 50px; font-size: 17px; font-weight: bold; display: inline-block; box-shadow: 0 4px 12px rgba(255,107,53,0.4); }
    .offer-box { background: #FFF8F5; border: 2px dashed #FF6B35; border-radius: 10px; padding: 18px 24px; text-align: center; margin: 24px 0; }
    .offer-box .code { font-size: 24px; font-weight: bold; color: #FF6B35; letter-spacing: 4px; }
    .offer-box p { margin: 4px 0 0; font-size: 13px; color: #888; }
    .footer { background: #222; color: #888; text-align: center; padding: 20px; font-size: 12px; }
    .footer a { color: #aaa; text-decoration: underline; }
  </style>
</head>
<body>
  <div class="wrapper">
    <div class="hero">
      <h1>50% OFF Everything</h1>
      <p>Our biggest sale of the year is finally here.</p>
      <span class="badge">⏰ ENDS IN 24 HOURS</span>
    </div>

    <div class="body">
      <h2>Hey, you don't want to miss this.</h2>
      <p>
        We're slashing prices across our entire store — for one day only.
        Whether you've been eyeing something for a while or just browsing,
        <strong>now is the time to grab it</strong> before it's gone.
      </p>

      <div class="features">
        <div class="feature">
          <div class="icon">🚀</div>
          <div class="label">Fast Delivery</div>
        </div>
        <div class="feature">
          <div class="icon">💯</div>
          <div class="label">Quality Guaranteed</div>
        </div>
        <div class="feature">
          <div class="icon">🔒</div>
          <div class="label">Secure Checkout</div>
        </div>
      </div>

      <div class="offer-box">
        <div class="code">SALE50</div>
        <p>Use this code at checkout to claim your 50% discount</p>
      </div>

      <div class="cta">
        <a href="#">Shop the Sale Now →</a>
      </div>
    </div>

    <div class="footer">
      You're receiving this because you subscribed to our newsletter.<br>
      <a href="#">Unsubscribe</a> &bull; <a href="#">View in browser</a><br><br>
      &copy; 2026 Octava Store &bull; Yogyakarta, Indonesia
    </div>
  </div>
</body>
</html>
"""

plain = "50% OFF Everything – Use code SALE50 at checkout. Ends in 24 hours. Shop now at octava.my.id"

msg = MIMEMultipart("alternative")
msg["From"] = SMTP_FROM
msg["To"] = to
msg["Subject"] = subject
msg.attach(MIMEText(plain, "plain"))
msg.attach(MIMEText(html, "html"))

print(f"Connecting to {SMTP_HOST}:{SMTP_PORT} ...")

with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(SMTP_USER, SMTP_PASSWORD)
    server.sendmail(SMTP_FROM, [to], msg.as_string())

print(f"✅ Email sent successfully to {to}")
