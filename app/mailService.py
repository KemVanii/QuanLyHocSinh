import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def send_email(students_data, subjectName, semester):
    # Mailtrap credentials
    smtp_host = 'smtp.mailtrap.io'
    smtp_port = 2525
    smtp_username = '1e937619c8e010'
    smtp_password = '1661971bb0b588'
    sender_email = 'quanlyhocsinh@uni.com'

    for student in students_data:
        recipient_email = student['email']

        # Email content
        subject = f"Bảng điểm học kì {semester} môn {subjectName}\n"
        body = f"Xin chào {student['student_name']},\n\n" \
               f"Bảng điểm học kì {semester} môn {subjectName}\n" \
               f"15p: {', '.join(map(str, student['15p']))}\n" \
               f"45p: {', '.join(map(str, student['45p']))}\n" \
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
                      f"15p: {', '.join(map(str, student['15p']))}\n" \
                      f"45p: {', '.join(map(str, student['45p']))}\n" \
                      f"CK: {student['ck']}\n" \
                      f"DTB: {student['dtb']}"
        scores_attachment = MIMEText(scores_text)
        scores_attachment.add_header('Content-Disposition', 'attachment',
                                     filename=f"{student['student_name']}_scores.txt")
        message.attach(scores_attachment)

        # Connect to Mailtrap's SMTP server
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)

            # Send email
            server.sendmail(sender_email, recipient_email, message.as_string())


# def send_otp(receiver_email, otp):
#     smtp_host = 'smtp.mailtrap.io'
#     smtp_port = 2525
#     smtp_username = '1e937619c8e010'
#     smtp_password = '1661971bb0b588'
#     sender_email = 'quanlyhocsinh@uni.com'
#     recipient_email = receiver_email
#
#     subject = "Mã otp"
#     body = f'Xin chao sau day la ma otp dang nhap \n' \
#            f'Ma otp la: {otp} \n' \
#            f'Vui long khong chia se voi nguoi khac.'
#
#     message = MIMEMultipart()
#     message['From'] = sender_email
#     message['To'] = recipient_email
#     message['Subject'] = subject
#     message.attach(MIMEText(body, 'plain'))
#
#     with smtplib.SMTP(smtp_host, smtp_port) as server:
#         server.starttls()
#         server.login(smtp_username, smtp_password)
#
#         # Send email
#         server.sendmail(sender_email, recipient_email, message.as_string())