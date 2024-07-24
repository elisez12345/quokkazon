from werkzeug.security import generate_password_hash
import csv,random,re
from faker import Faker
from collections import defaultdict
from datetime import datetime

num_users = 100
num_products = 200
num_purchases = 1000

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')

def gen_users(num_users):
    with open('Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{uid}'
            #password = generate_password_hash(plain_password)
            password = generate_password_hash("1234")
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            address = profile['address'].replace("\n"," ")
            phone_number=random.randint(1000000000, 9999999999)
            # print([uid,email,firstname,lastname,address,password,phone_number,0])
            writer.writerow([int(uid),email,firstname,lastname,address,password,phone_number,0])
        print(f'{num_users} generated')
    return

def fix_products_csv(file): 
    with open(file,"r") as f: 
        writer = get_csv_writer(open("Products.csv","w"))
        for line in f.readlines(): 
            info = line.split(",")
            # 1,Quokka Fur Brush,grooming,,A comb or something,12:58.0,12:58.0
            default_time = "2018-10-01 13:12:58"
            writer.writerow([info[0],info[1],info[2],info[3],info[4],default_time,default_time])

def get_available_products():
    available = defaultdict(dict)
    with open("Inventory.csv","r") as f: 
        info = f.readlines()
        for line in info: 
            # (sid, pid,quantity,num_for_sale,price)
            line = line.split(',')
            sid,pid,num_for_sale = line[0].replace("\"",''),line[1].replace("\"",''),line[3].replace("\"",'')
            available[pid][sid] = int(num_for_sale)
    return available 

# uid, sid, pid, order_id, time_purchased, quantity, date_fulfilled 
def gen_purchases(num_purchases, available):
    order_id = 0
    count = 0 
    with open('Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_purchases):
            if len(available) == 0: 
                # no more inventory left 
                break
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_element(elements=list(available.keys()))
            sid = random.choice(list(available[pid].keys()))
            order_id += 1  # TODO: order_id is not unique, should group purchases into orders
            quantity_available = available[pid][sid]
            quantity = fake.random_int(min=0,max=quantity_available)
            # ensure that items cannot be re-purchased 
            available[pid][sid] -= quantity
            if available[pid][sid] == 0: 
                del available[pid][sid] 
            if len(available[pid]) == 0: 
                del available[pid]

            time_purchased = "2023-10-25 13:12:58"
            date_fulfilled = "2023-10-27 13:12:58"  # TODO: change times, have some empty times for unfulfilled orders
            # time_purchased = fake.date_this_month().strftime("%Y-%m-%d %H:%M:%S")
            
            writer.writerow([uid, sid, pid, order_id, time_purchased,quantity,date_fulfilled])
            count += 1 
        print(f'{count} generated')
    return

def gen_sellers(num_users):
    with open('Sellers.csv','w') as f:
        writer = get_csv_writer(f)
        print('Sellers...', end=' ', flush=True)
        random.seed('quokka')
        num_sellers = 0
        for id in range(num_users):
            if random.random() < 0.2:
                writer.writerow([id])
                num_sellers += 1
        print(f'{num_sellers} users designated as sellers')
    return

def get_sellers(file):
    with open(file,'r') as f:
        return [int(sid.replace('"','').strip()) for sid in f.readlines()]

def get_pids(file):
    with open(file,'r') as f:
        return [int(line.split(',')[0]) for line in f.readlines()]

def gen_inventory():
    with open('Inventory.csv','w') as f:
        writer = get_csv_writer(f)
        print('Inventory...', end=' ', flush=True)
        random.seed('quokka')
        rows_added = 0
        for sid in get_sellers('/home/ubuntu/quokkazon/db/data/Sellers.csv'):
            num_items = random.randint(1,10)
            products = random.sample(get_pids('/home/ubuntu/quokkazon/db/data/Products.csv'),num_items)
            for pid in products:
                quantity = random.randint(0,1000)
                num_for_sale = random.randint(0,quantity)
                price = random.randint(0,30) + 0.99
                writer.writerow([sid, pid, quantity, num_for_sale, price])
                rows_added += 1
        print(f'{rows_added} enntries added to Inventory')
    return

def get_available_sellers(file):
    available = []
    with open(file,"r") as f: 
        info = f.readlines()
        for line in info: 
            sid = line.replace("\"","").strip()
            available.append(sid)
    return available

def gen_cart(num_users):
    with open('Cart.csv','w') as f:
        writer = get_csv_writer(f)
        print('Cart...', end=' ', flush=True)
        random.seed('quokka')
        available_sellers = get_available_sellers("/home/ubuntu/quokkazon/db/generated/Sellers.csv")
        for id in range(int(num_users)):
            uid = fake.random_int(min=0, max=num_users-1)
            sid = fake.random_element(elements=available_sellers)
            while(sid == uid):
                sid = fake.random_element(elements=available_sellers)
            pid = fake.random_int(min=1, max=253)
            quantity = fake.random_int(min = 1, max = 10)
            saved_for_later = 0
            writer.writerow([uid, sid, pid, quantity, saved_for_later])
            print(f'{num_users/2} generated')
        return


def gen_cart(num_users):
    with open('Cart.csv','w') as f:
        writer = get_csv_writer(f)
        print('Cart...', end=' ', flush=True)
        random.seed('quokka')
        available_sellers = get_available_sellers("/home/ubuntu/quokkazon/db/generated/Sellers.csv")
        for id in range(int(num_users)):
            uid = fake.random_int(min=0, max=num_users-1)
            sid = fake.random_element(elements=available_sellers)
            while(sid == uid):
                sid = fake.random_element(elements=available_sellers)
            pid = fake.random_int(min=1, max=253)
            quantity = fake.random_int(min = 1, max = 10)
            saved_for_later = 0
            writer.writerow([uid, sid, pid, quantity, saved_for_later])
            print(f'{num_users/2} generated')
        return

if __name__ == "__main__": 
    #gen_inventory()
    gen_users(num_users)
    available = get_available_products()
    gen_purchases(num_purchases, available)
    # fix_products_csv("/home/ubuntu/quokkazon/db/data/Products.csv")
