from django.shortcuts import render,HttpResponseRedirect
import MySQLdb
import datetime
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import simplejson as json
from datetime import date
from datetime import datetime
import datetime
import webbrowser

db = MySQLdb.connect('localhost','root','','harley')
c = db.cursor()

# Create your views here.

def sendsms(ph,msg):
    sendToPhoneNumber= "+91"+ph
    userid = "2000022557"
    passwd = "54321@lcc"
    url = "http://enterprise.smsgupshup.com/GatewayAPI/rest?method=sendMessage&send_to=" + sendToPhoneNumber + "&msg=" + msg + "&userid=" + userid + "&password=" + passwd + "&v=1.1&msg_type=TEXT&auth_scheme=PLAIN"
    # contents = urllib.request.urlopen(url)
    webbrowser.open(url)

def Customer_Registration(request):
    if request.POST:
        cname = request.POST.get("cname")
        address = request.POST.get("address")
        pincode = request.POST.get("pincode")
        gender = request.POST.get("gender")
        age = request.POST.get("age")
        district = request.POST.get("district")
        location = request.POST.get("location")
        email = request.POST.get("Email")
        mobile = request.POST.get("mobile")
        password = request.POST.get("Password")
        type= "Customer"

        # Check if email already exists in the table
        c.execute("SELECT email FROM cust_reg WHERE email=%s", [email])
        result = c.fetchone()
        if result:
            msg = "This email is already registered"
            return render(request, 'Customer Registration.html', {'msg': msg})

        # Insert new record into the table
        qry = "INSERT INTO cust_reg(cname,address,pincode,gender,age,district,location,email,mobile,password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (cname, address, pincode, gender, age, district, location, email, mobile, password)
        c.execute(qry, values)

        qr ="INSERT INTO login VALUES (%s, %s, %s)"
        values = (email, password, type)
        c.execute(qr, values)

        db.commit()
        return HttpResponseRedirect('/SignIn/')

    return render(request,'Customer Registration.html')

def SignIn(request):  
    msg=""
    request.session['username']=""
    request.session['NAME']=""
    request.session['uid']=""
    request.session['cid']=""
    request.session['sid']=""

    if request.POST:
        email = request.POST.get("email")
        password = request.POST.get("password")
        c.execute("select * from login where username='"+ email +"' and password='"+ password +"'")
        ds = c.fetchone()
        if ds:
            request.session['username']=email
            if ds[2] == 'Admin':
                return HttpResponseRedirect('/AdminHome/')
            elif ds[2] == 'Customer':
                c.execute("select * from cust_reg where email='"+email+"' and password='"+password+"'")
                ds = c.fetchone()
                request.session['uid'] = ds[0]
                request.session['NAME'] = ds[1]
                return HttpResponseRedirect('/CustomerHome/')
            elif ds[2] == 'Club':
                c.execute("select * from club_reg where email='"+email+"' and password='"+password+"' and status='Approve'")
                ds = c.fetchone()
                if ds:
                    request.session['cid'] = ds[0]
                    return HttpResponseRedirect('/ClubHome/')
                else:
                    msg="Waiting For Approval"
            elif ds[2] == 'Shop':
                c.execute("select * from shop_reg where email='"+email+"' and password='"+password+"'  and status='Accept'")
                ds = c.fetchone()
                if ds:
                    request.session['sid'] = ds[0]
                    return HttpResponseRedirect('/ShopHome/')
                else:
                    msg="Waiting For Approval"
        else:
            msg="Invalid username or password"
    return render(request,'Login.html',{"msg":msg}) 

def Club_Registration(request):
    if request.POST:
        cname = request.POST.get("cname")
        district = request.POST.get("district")
        location =request.POST.get("location")
        email =request.POST.get("Email")
        mobile= request.POST.get("mobile")
        regno = request.POST.get("regno")
        password = request.POST.get("Password")
        status = "Registered"
        type = "Club"
        qry = "insert into club_reg(clname,district,city,phone,email,reg_no,password,status) values('"+ cname +"','"+ district +"','"+ location +"','"+ mobile +"','"+ email +"','"+ regno +"','"+ password +"','"+ status +"')"
        qr ="insert into login values('"+ email +"','"+ password +"','"+ type +"')"
        c.execute(qry)
        c.execute(qr)
        db.commit()
        return HttpResponseRedirect('/SignIn/')
    return render(request,'Club Registration.html')   

def Shop_Registration(request):
    if request.POST:
        cname = request.POST.get("cname")
        district = request.POST.get("district")
        location = request.POST.get("location")
        email = request.POST.get("Email")
        mobile = request.POST.get("mobile")
        regno = request.POST.get("regno")
        password = request.POST.get("Password")
        qry = "insert into shop_reg(shop,district,city,phone,email,reg_no,password,status) values('"+ cname +"','"+ district +"','"+ location +"','"+ mobile +"','"+ email +"','"+ regno +"','"+ password +"','Registered')"
        qr = "insert into login values('"+ email +"','"+ password +"','Shop')"
        c.execute(qry)
        c.execute(qr)
        db.commit()
        return HttpResponseRedirect('/SignIn/')
    return render(request,'Shop Registration.html')
    
def Admin_Home(request):
    return render(request,'Admin Home.html') 

def Common_Home(request):
    return render(request,'Common Home.html')

def Club_Home(request):
    return render(request,'Club Home.html')

def Shop_Home(request):
    return render(request,'Shop Home.html')

def Customer_Home(request):
    return render(request,'Customer Home.html')

def About_Us(request):
    return render(request,'about.html') 

def Gallery(request):
    return render(request,'gallery.html') 

def Contact(request):
    if request.POST:
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        msg = request.POST.get("msg")
        qry = "insert into feedback(`name`,`phone`,`email`,`msg`) values ('"+str(name)+"','"+str(phone)+"','"+str(email)+"','"+str(msg)+"')"
        c.execute(qry)
        db.commit()
    return render(request,'contact.html')

def Admin_Add_Hospital(request):
    msg = ""
    if request.POST:
        name = request.POST.get("hname")
        adrs = request.POST.get("address")
        district = request.POST.get("district")
        location = request.POST.get("location")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        qry = "insert into hospital_reg(hname,address,district,location,phone,email) values('"+ name +"','"+ adrs +"','"+ district +"','"+ location +"','"+ phone +"','"+ email +"')"
        c.execute(qry)
        db.commit()
        msg = "Hospital Details Added Successfully."
    c.execute("select * from hospital_reg")
    data=c.fetchall() 
    return render(request,'Admin Add Hospital.html',{"data":data,"msg":msg})

def AdminRemoveHospital(request):
    if request.GET:
        a = request.GET.get('id')
        c.execute("delete from hospital_reg where hid = '"+str(a)+"'")
        db.commit()
        return HttpResponseRedirect("/AdminAddHospital/")
    return render(request,'AdminRemoveHospital.html')
        

def Admin_Add_Hotel(request):
    msg=""
    if request.POST:
        name = request.POST.get("hname")
        address = request.POST.get("address")
        dist = request.POST.get("district")
        loc = request.POST.get("location")
        pho = request.POST.get("phone")
        em = request.POST.get("email")
        qry="insert into hotel_reg(hotel,address,district,location,phone,email) values('"+ name +"','"+ address +"','"+ dist +"','"+ loc +"','"+ pho +"','"+ em +"')"
        c.execute(qry)
        db.commit()
        msg = "Hotel Details Added Successfully."
    c.execute("select * from hotel_reg")
    data=c.fetchall() 
    return render(request,'Admin Add Hotel.html',{"data":data,"msg":msg})

def AdminRemoveHotel(request):
    if request.GET:
        a = request.GET.get('id')
        c.execute("delete from hotel_reg where hoid = '"+str(a)+"'")
        db.commit()
        return HttpResponseRedirect("/AdminAddHotel/")
    return render(request,'AdminRemoveHotel.html')

def Admin_Add_Workshop(request):
    msg=""
    if request.POST:
        na = request.POST.get("hname")
        ad = request.POST.get("address")
        di = request.POST.get("district")
        lo = request.POST.get("location")
        ph = request.POST.get("phone")
        em = request.POST.get("email")
        qry="insert into workshop_reg(wname,address,district,location,phone,email) values('"+ na +"','"+ ad +"','"+ di +"','"+ lo +"','"+ ph +"','"+ em +"')"
        c.execute(qry)
        db.commit()
        msg = "Workshop Details Added Successfully."
    c.execute("select * from workshop_reg")
    data=c.fetchall() 
    return render(request,'Admin Add Workshop.html',{"data":data,"msg":msg})

def AdminRemoveWorkshop(request):
    if request.GET:
        a = request.GET.get('id')
        c.execute("delete from workshop_reg where wid = '"+str(a)+"'")
        db.commit()
        return HttpResponseRedirect("/AdminAddWorkshop/")
    return render(request,'AdminRemoveWorkshop.html')


def Admin_Add_Category(request):
    msg = ""
    if request.method == "POST":
        na = request.POST.get("cat_name")
        c.execute("SELECT * FROM categories WHERE cat_title = %s", (na,))
        category_exists = c.fetchone()
        if category_exists:
            msg = "Category Already Exists."
        else:
            qry = "INSERT INTO categories(cat_title) VALUES (%s)"
            c.execute(qry, (na,))
            db.commit()
            msg = "Category Added Successfully."
    c.execute("SELECT * FROM categories")
    data = c.fetchall()
    return render(request, 'Admin Add Category.html', {"data": data, "msg": msg})


def AdminRemoveCategory(request):
    if request.GET:
        a = request.GET.get('id')
        c.execute("delete from categories where cat_id = '"+str(a)+"'")
        db.commit()
        return HttpResponseRedirect("/AdminAddCategory/")
    return render(request,'AdminRemoveCategory.html')

def Admin_Add_Brand(request):
    msg = ""
    if request.method == "POST":
        na = request.POST.get("cat_name")
        c.execute("SELECT * FROM brands WHERE brand_title = %s", (na,))
        brand_exists = c.fetchone()
        if brand_exists:
            msg = "Brand Already Exists."
        else:
            qry = "INSERT INTO brands(brand_title) VALUES (%s)"
            c.execute(qry, (na,))
            db.commit()
            msg = "Brand Added Successfully."
    c.execute("SELECT * FROM brands")
    data = c.fetchall()
    return render(request, 'Admin Add Brand.html', {"data": data, "msg": msg})


def AdminRemoveBrand(request):
    if request.GET:
        a = request.GET.get('id')
        c.execute("delete from brands where brand_id = '"+str(a)+"'")
        db.commit()
        return HttpResponseRedirect("/AdminAddBrand/")
    return render(request,'AdminRemoveBrand.html')

def Admin_View_Customers(request):
    data = ""
    c.execute("select * from cust_reg")
    data=c.fetchall() 
    return render (request,"Admin View Customers.html",{"data":data})

def Admin_View_Feedback(request):
    data = ""
    c.execute("SELECT * FROM feedback")
    data = c.fetchall()
    if request.GET:
        a = request.GET.get('id')
        c.execute("delete from feedback where fid = '"+a+"'")
        db.commit()
        return HttpResponseRedirect("/AdminViewFeedback/")
    return render (request,"Admin View Feedback.html",{"data":data})

def Admin_View_Club(request):
    c.execute("SELECT * from club_reg where status = 'Registered'")
    data = c.fetchall()
    if request.GET:
        cl = request.GET.get('id')
        st = request.GET.get('st')
        c.execute("update club_reg set status = '"+st+"' where clid = '"+cl+"'")
        db.commit()
        return HttpResponseRedirect("/AdminViewClub/")
    return render(request,"Admin View Club.html",{"data":data})
    
def Admin_View_Shop(request):
    c.execute("SELECT * from shop_reg where status = 'Registered'")
    data = c.fetchall()
    if request.GET:
        cl = request.GET.get('id')
        st = request.GET.get('st')
        c.execute("update shop_reg set status = '"+st+"' where sid = '"+cl+"'")
        db.commit()
        return HttpResponseRedirect("/AdminViewShop/")
    return render(request,"Admin View Shop.html",{"data":data})

def Club_Add_Notification(request):
    msg=""
    clid = request.session['cid'] 
    if request.POST:
        a = request.POST.get('not')
        b = request.POST.get('da')
        date=datetime.date.today()
        qry = "insert into notification(notification,tripdate,notdate,clid) values('"+ a +"','"+ b +"','"+ str(date) +"','"+ str(clid) +"')"
        c.execute(qry)
        db.commit()
        msg = "Notification Added Successfully."
    c.execute("select * from notification where clid = '"+str(clid)+"'")
    data=c.fetchall() 
    return render(request,"Club Add Notification.html",{"data":data,"msg":msg})

def ClubRemoveNotification(request):
    if request.GET:
        a = request.GET.get('id')
        c.execute("delete from notification where notid = '"+str(a)+"'")
        db.commit()
        return HttpResponseRedirect("/ClubAddNotification/")
    return render(request,'ClubRemoveNotification.html')


def Club_View_Request(request):
    clid = request.session['cid']
    c.execute("SELECT clubjoin_req.*, cust_reg.*,club_reg.clid,club_reg.clname FROM clubjoin_req INNER JOIN cust_reg ON clubjoin_req.uid=cust_reg.cid inner join club_reg on club_reg.clid=clubjoin_req.clid where club_reg.clid = '"+str(clid)+"' and clubjoin_req.status = 'Request'")
    data = c.fetchall()
    if request.GET:
        cl = request.GET.get('id')
        st = request.GET.get('st')
        c.execute("update clubjoin_req set status = '"+st+"' where reid = '"+str(cl)+"'")
        db.commit()
        return HttpResponseRedirect("/ClubViewRequest/")
    return render(request,"Club View Request.html",{"data":data})


def RentStatus(request):
    cid = request.session['uid']
    c.execute("SELECT vehicle_rent.*, club_vehicle.ve_name AS vehicle_name FROM vehicle_rent JOIN club_vehicle ON vehicle_rent.veh_id = clve_id WHERE vehicle_rent.custid = '"+str(cid)+"'")
    data = c.fetchall()

    context = {'data': data}
    return render(request, 'ViewStatus.html', context)

def RentPay(request, id):
    c.execute("SELECT * from vehicle_rent WHERE rent_id = '"+str(id)+"'")
    data = c.fetchall()

    context = {'data': data}
    return render(request, 'RentPay.html', context)

def RentPaySuccess(request, id):
    c.execute("update vehicle_rent set pay = 1 where rent_id = '"+str(id)+"'")
    db.commit()

    return render(request, 'RentPaySuccess.html')

def RentDelete(request, id):
    print('rent id ',id)
    c.execute("delete from vehicle_rent where rent_id = '"+str(id)+"'")
    data = c.fetchall()

    return HttpResponseRedirect("/RentStatus/")


def Club_View_Riders(request):
    clid = request.session['cid']
    c.execute("SELECT clubjoin_req.*, cust_reg.*,club_reg.clid,club_reg.clname FROM clubjoin_req INNER JOIN cust_reg ON clubjoin_req.uid=cust_reg.cid inner join club_reg on club_reg.clid=clubjoin_req.clid where club_reg.clid = '"+str(clid)+"' and clubjoin_req.status = 'Accept'")
    data=c.fetchall()
    return render(request,"Club View Riders.html",{"data":data})

def Club_Add_Vehicle(request):
    msg=""
    clid = request.session['cid']
    if request.POST:
        name = request.POST.get('vname')
        cap = request.POST.get('cap')
        regno = request.POST.get('regno')
        rent = request.POST.get('rent')
        if request.POST and request.FILES:
            img=request.FILES.get("file")
            fs=FileSystemStorage()
            filename=fs.save(img.name,img)
            path=fs.url(filename)
            c.execute("insert into club_vehicle(clid,ve_name,cu_cap,reg_no,no_item,rent,img) values('" +str(clid) +"','"+name+"','"+cap+"','"+regno+"','1','"+rent+"','"+path+"')")
            db.commit()
            msg = "Vehicle Added Successfully."
    c.execute("select * from club_vehicle where clid = '"+str(clid)+"'")
    data=c.fetchall() 
    return render(request,'Club Add Vehicle.html',{"data":data,"msg":msg})

def ClubRemoveVehicle(request):
    if request.GET:
        a = request.GET.get('id')
        c.execute("delete from club_vehicle where clve_id = '"+str(a)+"'")
        db.commit()
        return HttpResponseRedirect("/ClubAddVehicle/")
    return render(request,'ClubRemoveVehicle.html')

def Club_View_Booking(request):
    clid = request.session['cid']
    c.execute("SELECT vehicle_rent.rent_id,club_vehicle.ve_name, cust_reg.cid,cust_reg.mobile, cust_reg.cname, club_vehicle.clve_id, vehicle_rent.pickup_date, vehicle_rent.return_date, vehicle_rent.cvrent_type, vehicle_rent.rent_unit, vehicle_rent.rent_days, vehicle_rent.amount, vehicle_rent.status FROM vehicle_rent INNER JOIN cust_reg ON vehicle_rent.custid = cust_reg.cid INNER JOIN club_vehicle ON vehicle_rent.veh_id = club_vehicle.clve_id AND vehicle_rent.clubid = club_vehicle.clid where club_vehicle.clid = '"+str(clid)+"' and vehicle_rent.status = 'Request'")
    print("SELECT vehicle_rent.rent_id,club_vehicle.ve_name, cust_reg.cid,cust_reg.mobile, cust_reg.cname, club_vehicle.clve_id, vehicle_rent.pickup_date, vehicle_rent.return_date, vehicle_rent.cvrent_type, vehicle_rent.rent_unit, vehicle_rent.rent_days, vehicle_rent.amount, vehicle_rent.status FROM vehicle_rent INNER JOIN cust_reg ON vehicle_rent.custid = cust_reg.cid INNER JOIN club_vehicle ON vehicle_rent.veh_id = club_vehicle.clve_id AND vehicle_rent.clubid = club_vehicle.clid where club_vehicle.clid = '"+str(clid)+"' and vehicle_rent.status = 'Request'")
    data=c.fetchall()
    msg=""
    if request.GET:
        cl = request.GET.get('id')
        st = request.GET.get('st')
        mo = request.GET.get('mo')
        if st =='Accept':
            c.execute("update vehicle_rent set status = '"+st+"' where rent_id = '"+str(cl)+"'")
            db.commit()
            msg = "Your rent request was approved successfully"
            #sendsms(mo,msg)
            return HttpResponseRedirect("/ClubViewBooking/")
        else:
            c.execute("update vehicle_rent set status = '"+'Reject'+"' where rent_id = '"+str(cl)+"'")
            db.commit()
            msg = "Your rent request was rejected"
            #sendsms(mo,msg)
            return HttpResponseRedirect("/ClubViewBooking/")
    return render(request,"Club View Booking.html",{"data":data})

def Customer_View_Profile(request):
    uid = request.session['uid']
    data=""
    if request.session['uid']:   
        c.execute(" select * from cust_reg where cid='"+str(uid)+"'")
        data=c.fetchall()
        if request.POST:
            Address=request.POST.get("Address")
            Phn=request.POST.get("Phn") 
            print(Phn)
            cvv="update cust_reg set mobile='"+Phn+"',address='"+Address+"' where cid='"+str(uid)+"'"
            print(cvv)
            c.execute(cvv)
            db.commit()
            return HttpResponseRedirect("/CustomerViewProfile/")
    return render (request,"Customer View Profile.html",{"data":data})

def Customer_View_Buy_Product(request):
    uid = request.session['uid']
    c.execute("SELECT * FROM customer_order WHERE uid='"+str(uid)+"'")
    data = c.fetchall()
    return render(request,"Customer View Buy Product.html",{"data":data})

def Customer_View_Notification(request):
    uid = request.session['uid']
    c.execute("SELECT club_reg.clid,club_reg.clname, notification.tripdate,  clubjoin_req.uid,  notification.notdate, notification.clid, notification.notification, notification.notid FROM club_reg INNER JOIN clubjoin_req ON club_reg.clid = clubjoin_req.clid INNER JOIN notification ON clubjoin_req.clid = notification.clid where clubjoin_req.status = 'Accept' and clubjoin_req.uid = '"+str(uid)+"'")
    data = c.fetchall()
    return render(request,"Customer View Notification.html",{"data":data})

def Customer_Search_Club(request):
    uid = request.session['uid']
    msg = ""

    if request.GET:
        a = request.GET.get('id')
        date = datetime.date.today()
        status = "Request"

        # Check if the user is already in the club
        c.execute("SELECT * FROM clubjoin_req WHERE clid = %s AND uid = %s", (a, uid))
        existing_request = c.fetchone()

        if existing_request:
            msg = "Already registred in the club"
        else:
            c.execute("INSERT INTO clubjoin_req(clid, uid, date, status) VALUES (%s, %s, %s, %s)",
                      (a, uid, date, status))
            db.commit()
            msg = "Request Sent Successfully"

    return render(request, 'Customer Search Club.html', {"msg": msg})


def subcat(request):
    catid=request.GET.get("dataid")
    c.execute("select * from club_reg where district='"+ str(catid)+"'")
    data=c.fetchall()
    return HttpResponse(json.dumps(data),content_type="application/json")

def CustomerSearchRentBike(request):
    # uid = request.session['uid']
    msg=""
    if request.GET:
        a = request.GET.get('id')
        date=datetime.date.today()
        status = "Request"
        c.execute("insert into clubjoin_req(clid,uid,date,status) values('"+str(a)+"','"+str(uid)+"','"+str(date)+"','"+status+"')")
        db.commit()
        msg = "Request Sent Successfully"
        return HttpResponseRedirect("/CustomerRentBikeRequest/")
    return render(request,'Customer Search Rent Bike.html',{"msg":msg})

def CustomerRentBikeRequest(request):
    vid = request.GET.get('id')
    total_amount=pd=rd=td=rt=days=""
    if 'Add' in request.POST:
        days=request.POST.get("tdate")
        pd=request.POST.get("pdate")
        rd=request.POST.get("rdate")
        td=request.POST.get("tdate")
        rt=request.POST.get("type")
        request.session["retp"]=rt
        c.execute("select rent from club_vehicle where clve_id = '"+str(vid)+"'")
        data=c.fetchone()
        amount=data[0]
        total_amount=int(days)*int(amount)
        request.session["tm"]=total_amount
    if 'sub' in request.POST:
        pd=request.POST.get("pdate")
        rd=request.POST.get("rdate")
        td=request.POST.get("tdate")
        rtp=request.session["retp"]
        cus = request.session["uid"]
        totam=request.session["tm"]
        c.execute("select clid from club_vehicle where clve_id = '"+str(vid)+"'")
        data = c.fetchone()
        clubid = data[0]
        c.execute("insert into vehicle_rent(veh_id,custid,clubid,pickup_date,return_date,cvrent_type,rent_unit,rent_days,amount,status) values('"+str(vid)+"','"+str(cus)+"','"+str(clubid)+"','"+str(pd)+"','"+str(rd)+"','"+str(rtp)+"','1','"+str(td)+"','"+str(totam)+"','Request')")
        db.commit()
        msg = "Rented Successfully"
        return render(request,'Customer Home.html',{"msg":msg})
    return render(request,'CustomerRentBikeRequest.html',{"total_amount":total_amount,"days":days,"pd":pd,"rd":rd,"td":td})

def subcatforbike(request):
    catid=request.GET.get("dataid")
    c.execute("SELECT club_vehicle.*, club_reg.* FROM club_vehicle INNER JOIN club_reg ON club_vehicle.clid=club_reg.clid  where club_reg.district='"+ str(catid)+"'")
    data=c.fetchall()
    return HttpResponse(json.dumps(data),content_type="application/json")

def CustomerShopping(Request):
    
    s="select * from products"
    c.execute(s)
    data=c.fetchall()
    t="select * from categories"
    c.execute(t)
    data1=c.fetchall()
    u="select * from brands"
    c.execute(u)
    data2=c.fetchall()
    return render(Request,'CustomerShopping.html',{"data":data,"data1":data1,"data2":data2})

def CustomerViewProCategory(Request):
    cname=Request.GET.get("id")
    # r="select catid from categories where product_cat='"+str(cname)+"'"
    # c.execute(r)
    # data=c.fetchone()
    # ci= data[0]
    s="select * from products where product_cat = '"+str(cname)+"'"
    c.execute(s)
    data=c.fetchall()
    t="select * from categories"
    c.execute(t)
    data1=c.fetchall()
    u="select * from brands"
    c.execute(u)
    data2=c.fetchall()
    
    return render(Request,'CustomerShopping.html',{"data":data,"data1":data1,"data2":data2})

def CustomerViewProSubCategory(Request):
    sid=Request.GET.get("id")
    s="select * from products where product_brand = '"+str(sid)+"'"
    c.execute(s)
    data=c.fetchall()
    t="select * from categories"
    c.execute(t)
    data1=c.fetchall()
    u="select * from brands"
    c.execute(u)
    data2=c.fetchall()
    return render(Request,'CustomerShopping.html',{"data":data,"data1":data1,"data2":data2})

def CustomerViewProDetails(Request):
    pid=Request.GET.get("id")
    s="select * from products where product_id = '"+str(pid)+"'"
    c.execute(s)
    data=c.fetchall()
    t="select * from categories"
    c.execute(t)
    data1=c.fetchall()
    u="select * from brands"
    c.execute(u)
    data2=c.fetchall()

    if(Request.POST):
        cid = Request.session["uid"]
        price = data[0][4]
        qty = Request.POST.get("qty")
        am = int(qty) * int(price)
        c.execute("insert into cart (cid,pid,qty,price)values('"+str(cid)+"','"+str(pid)+"','"+str(qty)+"','"+str(am)+"')")
        db.commit()
    return render(Request,'CustomerViewProDetails.html',{"data":data,"data1":data1,"data2":data2})

def CustomerOrderProduct(Request):
    pid=Request.GET.get("id")
    s="select * from products where pid = '"+str(pid)+"'"
    c.execute(s)
    data=c.fetchall()
    cid = Request.session["uid"]
    merid = data[0][8]
    price = data[0][6]
    c.execute("insert into cart (cid,fid,pid,amount,qty)values('"+str(cid)+"','"+str(merid)+"','"+str(pid)+"','"+str(price)+"','1')")
    db.commit()
    t="select * from categories"
    c.execute(t)
    data1=c.fetchall()
    u="select * from brands"
    c.execute(u)
    data2=c.fetchall()
    return render(Request,'CustomerViewProDetails.html',{"data":data,"data1":data1,"data2":data2})

def CustomerViewCart(Request):
    cid = Request.session["uid"]
    s="select * from cart inner join products on cart.pid = products.product_id where cart.cid = '"+str(cid)+"'"
    c.execute(s)
    data=c.fetchall()
    # merid = data[0][9]
    # price = data[0][6]
    # pid = data[0][3]
    # qty = data[0][5]
    t="select count(*) from cart where cid = '"+str(cid)+"'"
    c.execute(t)
    data1=c.fetchone()
    u="select sum(price) from cart where cid = '"+str(cid)+"'"
    c.execute(u)
    data2=c.fetchone()
    totalamount = data2[0]
    tot = totalamount
    Request.session["pay"] = str(tot)
    if Request.GET:
        ci = Request.GET.get('id')
        c.execute("delete from cart where id = '"+str(ci)+"'")
        db.commit()
        return HttpResponseRedirect("/CustomerViewCart")
    if(Request.POST):
        c.execute("select * from cart where cid = '"+str(cid)+"'")
        data3 = c.fetchall()
        for d3 in data3:
            custid = d3[1]
            proid = d3[2]
            amot = d3[4]
            quty = d3[3]
            carid = d3[0]
            c.execute("insert into customer_order (uid,pid,p_price,p_qty)values('"+str(custid)+"','"+str(proid)+"','"+str(amot)+"','"+str(quty)+"')")
            db.commit()
            c.execute("delete from cart where id = '"+str(carid)+"'")
            db.commit()
        return HttpResponseRedirect("/payment1")
    return render(Request,'CustomerViewCart.html',{"data":data,"data1":data1[0],"data2":data2[0]})

def payment1(request):
    
    if request.POST:
        card=request.POST.get("test")
        request.session["card"]=card
        cardno=request.POST.get("cardno")
        request.session["card_no"]=cardno
        pinno=request.POST.get("pinno")
        request.session["pinno"]=pinno
        return HttpResponseRedirect("/payment2")
    return render(request,"payment1.html")

def payment2(request):
    cno=request.session["card_no"]
    amount=request.session["pay"]
    if request.POST:
        # name=request.POST.get("t1")
        # request.session["m"]=name
        # address=request.POST.get("t2")
        # email=request.POST.get("t3")
        # phno=request.POST.get("t4")
        # n="insert into delivery values('"+str(cno)+"','"+str(name)+"','"+str(address)+"','"+str(email)+"','"+str(phno)+"','"+str(amount)+"')"
        # print(n)
        # c.execute(n)
        # con.commit()
        return HttpResponseRedirect("/payment3")
    return render(request,"payment2.html",{"cno":cno,"amount":amount})

def payment3(request):
    return render(request,"payment3.html")

def payment4(request):
    return render(request,"payment4.html")

def payment5(request):
    cno=request.session["card_no"]
    today = date.today()
    name =  request.session['NAME'] 
    amount = request.session["pay"]
    return render(request,"payment5.html",{"cno":cno,"today":today,"name":name,"amount":amount})

def CustomerViewMyBooking(request):
    cid=request.session["uid"]
    c.execute("select * from customer_order inner join products on customer_order.pid = products.product_id where customer_order.uid = '"+str(cid)+"'")
    data = c.fetchall()
    return render(request,"CustomerViewMyBooking.html",{"data":data})

def CustomerViewOrders(request):
    cid=request.session["uid"]
    c.execute("select * from customer_order inner join products on customer_order.pid = products.product_id inner join cust_reg on customer_order.uid = cust_reg.cid where customer_order.uid = '"+str(cid)+"'")
    data = c.fetchall()
    return render(request,"CustomerViewOrders.html",{"data":data})



def Shop_Add_Product(request):
    sid = request.session['sid']
    c.execute("select * from categories")
    data=c.fetchall()
    c.execute("select * from brands")
    data1=c.fetchall() 
    msg=""  
    if request.POST:
        a=request.POST.get("product_title")
        b=request.POST.get("cat_title")
        c1=request.POST.get("brand_title")   
        d=request.POST.get('price')
        e=request.POST.get('qty')
        f=request.POST.get('des')
        g=request.POST.get('key')
        if request.FILES.get("file"):
            myfile=request.FILES.get("file")
            fs=FileSystemStorage()
            filename=fs.save(myfile.name , myfile)
            uploaded_file_url = fs.url(filename)
            c.execute("insert into products(product_cat,product_brand,product_title,product_price,quantity,product_desc,product_image,product_keywords,shid) values('"+ str(b) +"','"+ str(c1) +"','"+ str(a) +"','"+ str(d) +"','"+ str(e) +"','"+ str(f) +"','"+ uploaded_file_url +"','"+ str(g) +"','"+ str(sid) +"')")
            db.commit()       
            msg = "Products Added Successfully."
    return render(request,"Shop Add Product.html",{"cat":data,"subcat":data1,"msg":msg})

def ShopRemoveProduct(request):
    if request.GET:
        a = request.GET.get('id')
        c.execute("delete from products where product_id = '"+str(a)+"'")
        db.commit()
        return HttpResponseRedirect("/ShopViewMyProduct/")
    return render(request,'ShopRemoveProduct.html')

def Shop_View_Orders(request):
    shid = request.session['sid']
    c.execute("SELECT customer_order.*, cust_reg.*,products.* FROM customer_order INNER JOIN cust_reg ON customer_order.uid=cust_reg.cid inner join products on products.product_id=customer_order.pid where products.shid = '"+str(shid)+"'")
    data = c.fetchall()
    return render(request,"Shop View Orders.html",{"data":data})

def Shop_View_My_Product(request):
    shid = request.session['sid']
    c.execute("select * from products where shid = '"+str(shid)+"'")
    data = c.fetchall()
    if request.GET:
        return HttpResponseRedirect("/ShopUpdateProduct/")
    return render(request,"Shop View My Product.html",{"data":data})

def ShopUpdateProduct(request):
    pid = request.GET.get('id')
    c.execute("select * from products where product_id = '"+str(pid)+"'")
    data = c.fetchall()
    if request.POST:
            price=request.POST.get("price")
            qty=request.POST.get("qty") 
            c.execute("update products set product_price = '"+str(price)+"', quantity = '"+str(qty)+"' where product_id = '"+str(pid)+"'")
            db.commit()
            return HttpResponseRedirect("/ShopViewMyProduct/")
    return render(request,"ShopUpdateProduct.html",{"data":data})

def Map(request):
    return render(request,'Map.html')
        


def customer_View_hospital(request):
    data = ""
    c.execute("select * from hospital_reg")
    data=c.fetchall() 
    return render (request,"customer_view_hospital.html",{"data":data})

def customer_View_hotel(request):
    data = ""
    c.execute("select * from hotel_reg")
    data=c.fetchall() 
    return render (request,"customer_view_hostel.html",{"data":data})

def customer_View_workshop(request):
    data = ""
    c.execute("select * from workshop_reg")
    data=c.fetchall() 
    return render (request,"customer_view_workshop.html",{"data":data})





  
def guestviewshop(request):
    c.execute("SELECT * from shop_reg ")
    data = c.fetchall()
    
    return render(request,"guestviewshop.html",{"data":data})


def guestviewclub(request):
    c.execute("SELECT * from club_reg where status = 'Registered'")
    data = c.fetchall()
    
    return render(request,"guestviewclub.html",{"data":data})


def guestviewproduct(Request):
    
    s="select * from products"
    c.execute(s)
    data=c.fetchall()
    t="select * from categories"
    c.execute(t)
    data1=c.fetchall()
    u="select * from brands"
    c.execute(u)
    data2=c.fetchall()
    return render(Request,'guestviewproduct.html',{"data":data,"data1":data1,"data2":data2})

