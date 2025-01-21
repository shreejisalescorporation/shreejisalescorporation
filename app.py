from flask import Flask,request,render_template,jsonify
from flask_cors import CORS
import smtplib
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
load_dotenv()



app = Flask(__name__, template_folder='templates', static_folder='static')  # Contact.html is in website directorystatic_folder='website')
CORS(app, origins=["https://shreejisalescorp.in"])


@app.route('/')
def inquiryform():
    return render_template('contact.html')  # Load the contact.html file

@app.route('/send_inquiry', methods=['POST'])
def send_inquiry():
    name = request.form['name']
    email = request.form['email']
    phoneno=request.form['phone']
    city=request.form['city']
    selectedproducts=request.form.getlist("product[]")
    product=",".join(selectedproducts)
    message = request.form['message']



    # reCAPTCHA verification
    recaptcha_response = request.form.get('g-recaptcha-response')
    if not recaptcha_response:
        return jsonify({"status": "error", "message": "Missing reCAPTCHA response."})

    secret_key = os.getenv("secretkeycap")  # Store your secret key in .env
    # Verify reCAPTCHA response with Google API
    verify_url = "https://www.google.com/recaptcha/api/siteverify"
    response = requests.post(
        verify_url,
        data={"secret": secret_key, "response": recaptcha_response}
    )
    result = response.json()

    if not result.get('success'):
        return jsonify({'error': 'reCAPTCHA verification failed. Please try again.'})


 












    # Your email details
    sender_email =os.getenv("email")  # Replace with your email
    sender_password =os.getenv("emailpass")  # Replace with your email password
    receiver_email =os.getenv("email")  # Replace with the receiver's email

    subject = "New Inquiry from Website"
    email_body = f"""
    You have received a new inquiry:
    
    Name: {name}
    Email: {email}
    Phone: {phoneno}
    City: {city}
    Product: {(product[:])}
    Message: {message}
    """

    try:
        # Set up the SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)

        # Create email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(email_body, 'plain'))
        # Send email
        server.send_message(msg)



        # Now send a confirmation email to the person who submitted the inquiry
        confirmation_subject = "Confirmation: Your Inquiry Has Been Received"
        confirmation_body = f"""
        Dear {name},

        Thank you for reaching out to us. We have received your inquiry and 
        will get back to you shortly.

        Here is a copy of your inquiry:
        
        Name: {name}
        Email: {email}
        Phone: {phoneno}
        City: {city}
        Product: {(product[:])}
        Message: {message}

        Best regards,
        Shreeji Sales Corporation
        """

        # Create the email for the user (confirmation email)
        confirmation_msg = MIMEMultipart()
        confirmation_msg['From'] = sender_email
        confirmation_msg['To'] = email  # Send to the user's email
        confirmation_msg['Subject'] = confirmation_subject
        confirmation_msg.attach(MIMEText(confirmation_body, 'plain'))

        # Send the confirmation email
        server.send_message(confirmation_msg)









        server.quit()
        return jsonify({"status": "success", "message": "Inquiry sent successfully!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run() 
