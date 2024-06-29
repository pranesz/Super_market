import datetime
import smtplib
import random

def load_menu_file(filename):
    menu = {}
    current_category = None
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if ',' in line:
                    item, price = line.split(',')
                    if current_category is not None:
                        menu[current_category][item] = int(price)
                else:
                    current_category = line
                    menu[current_category] = {}
        return menu
    except FileNotFoundError:
        print("Menu file not found. Using default menu.")
    except Exception as e:
        print(f"An error occurred while reading the menu file: {e}")

def send_mail(to_mail, subject, message):
    try:
        s = smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        s.login("email@gmail.com","password")
        email_message = f"Subjects: {subject}\n\n{message}"
        s.sendmail("praneshpranesh648@gmail.com",to_mail,email_message)
        s.quit()
        print("Mail send succesfully")
    except Exception as e:
        print(f"Mail not send due to {e}")

def generate_otp(email):
    otp = random.randint(0000,9999)
    subject = 'Your Otp from Pranesz Super Market'
    message = f'Your otp number is {otp}'
    send_mail(email,subject,message)
    return otp

def generate_bill():
    print("Welcome to Pranez Super Market")
    username = input("Enter Your name: ")
    email = input("Enter you email id: ")

    otp  = generate_otp(email)
    if otp is None:
        print("Failed to send otp")
    user_otp = int(input("enter your otp number: "))
    if otp != user_otp:
        print(f"Incorrect otp {otp}")
        return
    with open("login.txt", "w") as f:
        f.write(username +'\n')
        f.write(email +'\n')

    menu = load_menu_file('menu.txt')
    if not menu:
        print("Failed to load menu. Exiting.")
        return

    discount = 5 / 100
    gst = 3 / 100
    order = {}

    while True:
        print("\nAvailable Categories:")
        for category in menu.keys():
            print(f"- {category}")
        
        select_category = input("Enter category (or 'done' to finish): ").strip().lower()
        if select_category == 'done':
            break

        if select_category in menu:
            print(f"Yes, {select_category} is available.")
            for item, price in menu[select_category].items():
                print(f'{item}: {price}')
        else:
            print(f"Sorry, {select_category} is not available.")
            continue
        
        your_order = input("Enter what you want to order (or 'back' to go to categories): ").strip().lower()

        if your_order == 'back':
            continue

        if your_order in menu[select_category]:
            print(f"Yes, {your_order} is available.")
            try:
                how_many = int(input(f"Enter how many {your_order} you want: "))
                if your_order in order:
                    order[your_order] += how_many
                else:
                    order[your_order] = how_many
            except ValueError:
                print("Please enter a valid number.")
        else:
            print(f"Sorry, {your_order} is not available in {select_category}.")
        
    
    total = 0
    bill_details = f"Bill for {username}\n\nItems purchased:\n"
    for item, quantity in order.items():
        for category in menu:
            if item in menu[category]:
                item_price = menu[category][item]
                bill_details += f"{item}: {quantity} x {item_price} = {quantity * item_price}\n"
                total += item_price * quantity
                break

    discount_amount = total * discount
    discount_total = total - discount_amount
    gst_amount = discount_total * gst
    total_payable = discount_total + gst_amount  

    date = datetime.datetime.now()
    formatted_date = date.strftime('%Y-%m-%d %H:%M:%S')
    day = date.strftime("%A")
    
    bill_details += f"\nTotal amount: {total}\n"
    bill_details += f"Discount ({discount * 100}%): -{discount_amount}\n"
    bill_details += f"Amount after discount: {discount_total}\n"
    bill_details += f"GST ({gst * 100}%): +{gst_amount}\n"
    bill_details += f"Total payable: {total_payable}\n"
    bill_details += f"\n\nBill generated on {formatted_date} ({day})\n"

    with open('payment.txt','w') as f:
        f.write(bill_details)
    
    print("Bill successfully Generated")
    print(bill_details)

    send_mail(email, "Your Bill From Pranesz Super Market",bill_details)

generate_bill()
