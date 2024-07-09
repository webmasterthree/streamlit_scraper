import re
def get_emails(html):
    print("Getting Mails...")
    email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,4}"
    emails = re.findall(email_pattern, html)

    # print("Emails: ", emails)

    return emails


def get_phones(html):
    print("Getting Phone Numbers...")
    cleaned_text = html.replace(' ', '').replace('-', '')
    numbers = re.findall(r'\d{10,12}', cleaned_text)

    for i in range(len(numbers)):
        if numbers[i][0] == '0':
            if len(numbers[i]) > 11:
                numbers[i] = ''
                continue
        
        if numbers[i][0] != '9':
            if len(numbers[i]) >= 12:
                numbers[i] = ''
                continue
        
        if len(numbers[i]) == 10:
            if numbers[i][0] != '0' and numbers[i][0] != '9' and numbers[i][0] != '8' and numbers[i][0] != '7':
                numbers[i] = ''
                continue
            
    
    numbers = [number for number in numbers if number != '']

    # print("Phone Numbers: ", numbers)
    
    return numbers