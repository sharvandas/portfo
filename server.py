from flask import Flask, render_template, request, redirect
import json
import smtplib

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template('index.html')


@app.route("/<string:page_name>")
def html_page(page_name=None):
    return render_template(f'{page_name}')


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        print(email, message, subject)
        new_data = {
            email:
                {
                    "subject":subject,
                    "message":message
                }
        }
        print("new data:",new_data)
        try:
            with open('data_stored.json', "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open('data_stored.json', "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        except Exception as e:
            print("Found Error with something", e)
        else:
            data.update(new_data)
            with open("data_stored.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user = "snrjds@gmail.com", password="iunvwpqbfaaxjlni")
                connection.sendmail(from_addr="snrjds@gmail.com", to_addrs="snrjds@yahoo.com",
                                    msg=f"Subject:{subject} \n\n {message} \n we got this message from email id: {email}")
                print("message sent")

        return redirect('thank_you.html')
    else:
        return 'something went wrong'
