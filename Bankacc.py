import mysql.connector as sq
import datetime
import sys
import random
from prettytable import PrettyTable
bank=sq.connect(user='root',password='',host='localhost',database='bank',charset='utf8')
mycursor=bank.cursor()
def menu ():
    print('BANK ACCOUNT SOFTWARE'.center(120))
    print('-*-'*44)
    print('WELCOME'.center(120))
    print('''MAIN MENU
             1.Open Account
             2. Display Account
             3. Modify Account
             4. Withdraw Money
             5. Deposit Money
             6. Display Passbook
             7. Close Account
             8. Exit''')
    choice=int(input('Enter your choice'))
    while True:
        if choice==1:
            create()
        elif choice==2:
            display()
        elif choice==3:
            Modify()
        elif choice==7:
            close()
        elif choice==8:
            print('Exiting...')
            bank.close()
            sys.exit()
        elif choice==4:
            withdraw()
        elif choice==5:
            deposit()
        elif choice==6:
            dis_pass()
        else:
            print('Wrong Choice!')
            menu()
def create():
    try:
        cmd='''create table bankacc (AcNo varchar(15) primary key,Name varchar(20),Address varchar(20),Email varchar(20),Mobile varchar(10),Amount varchar(131),Type char(20))'''
        mycursor.execute(cmd)
        cmd='''create table passbook (AcNo varchar(15) ,Date date ,Debit integer,Credit integer,Balance integer,Particular char(20))'''
        mycursor.execute(cmd)
        open()
    except:
        Open()
def Open():
    while True:
        acc=random.randint(11111111,99999999)
        Name=str(input('Enter Name'))
        add=input('Enter Address')
        email=input('Enter Your Email')
        mob=int(input('Enter Your Mobile No.'))
        amt=amount()
        typea=typ()
        rec=(acc,Name,add,email,mob,amt,typea)
        cmd='insert into bankacc values(%s,%s,%s,%s,%s,%s,%s)'
        c=bank.cursor()
        c.execute(cmd,rec)
        bank.commit()
        print('Your Account no. is --->',acc)
        ch=input('Do you want to enter more records (y/n)')
        if ch=='n' or ch=='N':
            break
    menu()
def amount():
    a=int(input('Enter opening Amount'))
    s=0
    if a>=5000:
        s+=a
    else:
        print('Minimum opening amount is 5000 Rs.')
        s=amount()
    return s
def typ():
    print('''Enter from the given choice which type of Account you want to open
                                     1. FD
                                     2. Saving
                                     3. Current''')
    typ1=int(input('Enter(1/2/3)'))
    a=''
    if typ1==1:
        a+='FD'
    elif typ1==2:
        a+='Saving'
    elif typ1==3:
        a+='Current'
    else:
        print('wrong choice')
        typ()
    return a
def display():
    mycursor.execute('select*from bankacc')
    d=mycursor.fetchall()
    ac=str(input('enter your account no.'))
    for i in d:
        if i[0]==ac:
            print('Account no.-->',i[0])
            print('Name-->',i[1])
            print('Address-->',i[2])
            print('Email-->',i[3])
            print('Mobile-->',i[4])
            print('Amount-->','₹',i[5])
            print('Type-->',i[6])
            break
    else:
        print('Account no. not found')
    menu()
def Modify():
    mycursor.execute('select*from bankacc')
    d=mycursor.fetchall()
    ac=str(input('enter your account no.'))
    f=False
    for i in d:
        if i[0]==ac:
            f=True
            while True:
                print('''what you want to modify
                Press   1.To Change Name
                           2. To change address
                           3.To Change Mobile no
                           4.To Change email
                           5. To Change Type of account''')
                c=int(input('enter your choice'))
                if c==1:
                    Name=str(input('enter new name'))
                    cmd='update bankacc set name=%s where acno=%s'
                    rec=(Name,i[0])
                    mycursor.execute(cmd,rec)
                    bank.commit()
                    print('Name updated!')
                elif c==2:
                    ad=str(input('enter new address'))
                    cmd='update bankacc set address=%s where acno=%s'
                    rec=(ad,ac)
                    mycursor.execute(cmd,rec)
                    bank.commit()
                    print('Address updated!')
                elif c==3:
                    mob=int(input('enter new mobile no.'))
                    cmd='update bankacc set mobile=%s where acno=%s'
                    rec=(mob,ac)
                    mycursor.execute(cmd,rec)
                    bank.commit()
                    print('mobile no. updated!')
                elif c==4:
                    em=str(input('enter new email'))
                    cmd='update bankacc set email=%s where acno=%s'
                    rec=(em,ac)
                    mycursor.execute(cmd,rec)
                    bank.commit()
                    print('email updated!')
                elif c==5:
                    ty=typ()
                    cmd='update bankacc set type=%s where acno=%s'
                    rec=(ty,ac)
                    mycursor.execute(cmd,rec)
                    bank.commit()
                    print('Account type updated!')
                else:
                    print('Please select right choice')
                    continue
                w=str(input('want to update more records(y/n)'))
                if w=='n' or w=='N':
                    break
    if f==True:
        menu()
    else:
        print('Wrong Account No.!')     
    menu()
def close():
    mycursor.execute('select*from bankacc')
    d=mycursor.fetchall()
    ac=str(input('enter Your account no. to be Close'))
    for i in d:
        if i[0]==ac:
            cmd='delete from bankacc where acno=%s'
            rec=(i[0],)
            mycursor.execute(cmd,rec)
            bank.commit()
            print('Account deleted!')
            break
    else:
        print('Account no. not matched!!')
    menu()
def money():
    a=''
    print('''select your choice
                               1.By Cash
                               2.By cheque
                               3.NEFT''')
    c=int(input('Enter(1/2/3)'))
    if c==1:
        a+='Cash'
    elif c==2:
        a+='Cheque'
    elif c==3:
        a+='NEFT'
    else:
        print('Wrong choice')
        print('Enter again!')
        money()
    return a
def withdraw():
    mycursor.execute('select*from bankacc')
    d=mycursor.fetchall()
    ac=str(input('enter your account no.'))
    found=True
    s=True
    t=True
    for i in d:
        if i[0]==ac:
            q=int(i[5])
            wi=int(input('enter money you want to withdraw'))
            if (int(i[5])-wi)>=5000:
                found=False
                cmd='update bankacc set amount=amount-%s where acno=%s'
                rec=(wi,i[0])
                mycursor.execute(cmd,rec)
                bank.commit()
                d=sam()
                u=q-wi
                re=(d,wi,i[0],u)
                cm='Insert into passbook (date,debit,acno,balance) values (%s,%s,%s,%s)'
                mycursor.execute(cm,re)
                bank.commit()
            elif int(i[5])<wi:
                t=False
            else:
                s=False
    if found==False:
        print('₹',wi,'withdraw successfully')
    elif s==False:
        print('Your bank balance should have minimum of ₹5000')
    elif t==False:
        print('Your account balance is only',q)
    else:
        print("Wrong account no.")
    menu()
def sam():
    mycursor.execute('select curdate()')
    da=mycursor.fetchone()
    dat=da[0]
    return dat
def deposit():
    mycursor.execute('select*from bankacc')
    d=mycursor.fetchall()
    ac=str(input('enter your account no.'))
    my=money()
    f=False
    for i in d:
        if i[0]==ac:
            f=True
            wi=int(input('enter money you want to deposit'))
            cmd='update bankacc set amount=amount+%s where acno=%s'
            rec=(wi,i[0])
            mycursor.execute(cmd,rec)
            bank.commit()
            de=sam()
            s=wi+int(i[5])
            re=(de,wi,i[0],my,s)
            cm='Insert into passbook (date,credit,acno,Particular,balance) values (%s,%s,%s,%s,%s)'
            mycursor.execute(cm,re)
            bank.commit()
    if f==False:
        print('Account no. not matched')
    else:
        print('₹',wi,'Credited successfully','by',my)
    menu()
def dis_pass():
    c=str(input('enter your account no.'))
    mycursor.execute('Select*from bankacc')
    d=mycursor.fetchall()
    mycursor.execute('Select*from passbook')
    e=mycursor.fetchall()
    f=False
    s=False
    for j in d:
        if j[0]==c:
            s=True
    l=PrettyTable(['Date', 'Debit', 'Credit', 'Mode', 'Balance'])
    for i in e:
        if i[0]==c:
            f=True
            l.add_row([i[1], i[2], i[3], i[5], i[4]])
            #print('Date -->',i[1],'Debit--> ₹',i[2],'Credit--> ₹',i[3],'Mode-->',i[5],'Balance--> ₹',i[4])
    print(l)
    if s==False:
        print('Wrong Account no.')
    elif f==False:
        print('No Transaction')
    else:
        menu()
    menu()
menu()