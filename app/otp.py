import pyotp
from app import mailService
from vonage import Client, Sms

# Thông tin tài khoản Nexmo
client = Client(key="7e5dddec", secret="YETOQbF0365stjCm")
sms = Sms(client)


def send_sms_nexmo(phone_number, otp):
    responseData = sms.send_message(
        {
            "from": "Vonage APIs",
            "to": phone_number,
            "text": f'Ma otp cua ban la: {otp}. Vui long khong chia se cho nguoi khac',
        }
    )

    if responseData["messages"][0]["status"] == "0":
        print("Message sent successfully.")
    else:
        print(f"Message failed with error: {responseData['messages'][0]['error-text']}")


def generate_otp():
    # Tạo secret key cho người dùng mới
    secret_key = pyotp.random_base32()

    # Tạo đối tượng TOTP từ secret key
    totp = pyotp.TOTP(secret_key)

    # Lấy mã OTP hiện tại
    otp = totp.now()

    return secret_key, otp


def verify_otp(secret_key, user_input_otp):
    # Tạo đối tượng TOTP từ secret key đã lưu trữ
    totp = pyotp.TOTP(secret_key)

    # Xác thực mã OTP từ người dùng nhập vào
    is_valid = totp.verify(user_input_otp)

    return is_valid


if __name__ == '__main__':
    key = generate_otp()
    send_sms_nexmo(phone_number='84923923779', otp=key[1])
