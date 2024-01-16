import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def send_email(students_data, subjectName, semester):
    # Mailtrap credentials
    smtp_host = 'smtp.mailtrap.io'
    smtp_port = 2525
    smtp_username = '6ec9b93cc05cf9'
    smtp_password = 'd1b842c7290687'
    sender_email = 'quanlyhocsinh@uni.com'

    # Connect to Mailtrap's SMTP server
    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        # Send email
        for student in students_data:
            recipient_email = student['email']

            # Email content
            subject = f"Bảng điểm học kì {semester} môn {subjectName}\n"
            body = f"Xin chào {student['student_name']},\n\n" \
                   f"Bảng điểm học kì {semester} môn {subjectName}\n" \
                   f"15p: {', '.join(student['15p'])}\n" \
                   f"45p: {', '.join(student['45p'])}\n" \
                   f"CK: {student['ck']}\n" \
                   f"DTB: {student['dtb']}\n\n" \
                   f"Trân trọng"
            # Create MIME object
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = recipient_email
            message['Subject'] = subject
            message.attach(MIMEText(body, 'plain'))

            # Attach scores as a text file
            scores_text = f"Bảng điểm học kì {semester} môn {subjectName}\n" \
                          f"15p: {', '.join(student['15p'])}\n" \
                          f"45p: {', '.join(student['45p'])}\n" \
                          f"CK: {student['ck']}\n" \
                          f"DTB: {student['dtb']}"
            scores_attachment = MIMEText(scores_text)
            scores_attachment.add_header('Content-Disposition', 'attachment',
                                         filename=f"{student['student_name']}_scores.txt")
            message.attach(scores_attachment)
            server.sendmail(sender_email, recipient_email, message.as_string())
