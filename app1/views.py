from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from .forms import Company_forms
from django.contrib.auth.decorators import login_required
from .models import Company,Common_User,Invest
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.
def log_in(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']
        if email and password:
            user=authenticate(email=email,password=password)
            if user:
                if user.is_superuser:
                    login(request,user=user)
                    return render(request,'awelcome.html',{'user':user.username})
                messages.error(request,'is not a admin')
                return redirect('admin1')
            messages.error(request,'password and  email is worng')
            return  redirect('admin1')
        messages.error(request,'password and email is wrong')
        return redirect('admin1')
    return render(request,'login.html')

@login_required(login_url='/ad/')
def add_company(request):
    if request.method=="POST":
        form=Company_forms(request.POST)
        price=request.POST.get('share_price')
        print(price,type(price))
        if int(price)<=699:
            if form.is_valid():
                form.save()
                messages.success(request,'details are saved')
                return redirect('addc')
            messages.error(request,'details are not saved')
            return redirect('addc')
        messages.error(request,'share value not greatethan 699')
        return redirect('addc')
    form=Company_forms()
    return render(request,'addcompany.html',{"form":form})

@login_required(login_url='/ad/')
def list_compay(request):
    qs=Company.objects.all()
    return render(request,'list_co.html',{'data':qs})

@login_required(login_url='/ad/')
def udpate_comay(request,id):
    user=request.user
    print(user.id)
    if user:
        data=get_object_or_404(Company,id=id)
        if request.method=="POST":
            form=Company_forms(request.POST,instance=data)
            price=request.POST['share_price']
            company_name=request.POST['name']
            name=Company.objects.get(name=company_name)
            print(name)
            print(data.share_price-int(price))
            if int(price)<=699:
                if data.share_price == int(price):
                    if form.is_valid():
                        form.save()
                        messages.success(request,'details are updated')
                        return redirect('listco')

                elif (data.share_price-int(price))>0:
                    inv=Invest.objects.filter(company_name_id=name.id)
                    for x in inv:
                        id=x.user_id
                        com=Common_User.objects.filter(user_id=id)
                        com1=com.get(user_id=id)
                        diff=data.share_price-int(price)
                        com.update(invested=(com1.invested+(x.noofsahes*diff)))
                    if form.is_valid():
                        form.save()
                        messages.success(request, 'details are updated')
                        return redirect('listco')
                else:
                    inv = Invest.objects.filter(company_name_id=name.id)
                    for x in inv:
                        id=x.user_id
                        com = Common_User.objects.filter(user_id=id)
                        com1 = com.get(user_id=id)
                        diff = data.share_price - int(price)
                        com.update(invested=(com1.invested +(x.noofsahes* diff)))
                    if form.is_valid():
                        form.save()
                        messages.success(request, 'details are updated')
                        return redirect('listco')

                messages.error(request,'details are not saved')
                return redirect('listco')
            messages.error(request,'share_value is  not > 699')
            return redirect('listco')
        form=Company_forms(instance=data)
        return render(request,'updatedd.html',{'form':form})

@login_required(login_url='/ad/')
def delete_comay(request,id):
    data=get_object_or_404(Company,id=id)
    # print(type(data.share_price))
    # print(data.name)
    # print(data.id)
    data1=Invest.objects.filter(company_name_id=data.id)
    for x in data1:
        print(type(x.noofsahes))
        u=Common_User.objects.filter(user_id=x.user_id)
        k=u.get(user_id=x.user_id)
        u.update(invested=k.invested+(data.share_price*x.noofsahes))


    data.delete()
    return redirect('list')


def log_out(request):
    user=request.user
    if user:
        logout(request)
        return redirect('admin1')


def log_in_user(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']
        if email and password:
            user=authenticate(email=email,password=password)
            if user:
                if not user.is_superuser:
                    login(request,user=user)
                    return render(request,'welcomeuser.html',{"user":user.username})
                messages.error(request,'is not a superuser')
                return redirect('user')
            messages.error(request,'email and password is wrong ')
            return redirect('user')
        messages.error(request,'email and password is not wrong')
        return redirect('user')

    return render(request,'loginuser.html')


def register(request):
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        re_password=request.POST['re_password']
        if password == re_password:
            if User.objects.filter(email=email).exists():
                messages.success(request,'email is alreay exists')
                return redirect('regi')

            user=User.objects.create_user(username=username,email=email,password=password)
            print(user.id)
            user.save()

            Common_User(invested=100000,user_id=user.id).save()
            messages.success(request,'details are saved')
            return redirect('regi')
        messages.error(request,'password and re_password is not equal')
        return redirect('regi')
    return render(request,'register1.html')

@login_required(login_url='/user/')
def create_investmet(request):
    user=request.user
    if not user.is_superuser:
        print(user.id)
        if request.method=="POST":
            company_name=request.POST['company_name']
            noofshares=request.POST['noofshares']
            data=Company.objects.filter(name=company_name)
            data1=data.get(name=company_name)
            price=data1.share_price*int(noofshares)
            print(price,type(price))
            id=Common_User.objects.filter(user_id=user.id)
            id1=id.get(user_id=user.id)
            total=id1.invested-price

            if id1.invested>=price:
                Invest(user_id=user.id,company_name_id=data1.id,noofsahes=noofshares).save()
                id.update(invested=total)
                messages.success(request,'details are saved')
                return redirect('create')
            messages.success(request,'not saved')
            return redirect('create')
        qs=Company.objects.all()
        return render(request,'investcreate.html',{"qs":qs})
    else:
        return redirect('user')

@login_required(login_url='/user/')
def list_investmet(request):
    user=request.user
    qs=Invest.objects.filter(user_id=user.id)
    total_investmet=0
    for x in qs:
        total_investmet=total_investmet+(x.company_name.share_price*x.noofsahes)

    return render(request,'list_inve.html',{'qs':qs,'total_investment':total_investmet,'user':user.username})

@login_required(login_url='/user/')
def udpate_investe(request,id):
    id1=get_object_or_404(Invest,id=id)
    user=request.user
    print(user.id)
    if request.method=="POST":
        company_name=request.POST['company_name']
        noofshares=request.POST['noofshares']
        data=Company.objects.filter(name=company_name)
        data1 = data.get(name=company_name)
        print(data1)
        id=Common_User.objects.filter(user_id=id1.user_id)
        min=id.get(user_id=id1.user_id)
        print('min',min.id)

        noof=id1.noofsahes
        print(noof)
        price=id1.company_name.share_price
        print(price)
        old=min.invested+price*noof
        print(old)
        minn=id.update(invested=old)
        print('minnn',minn)
        minn=Common_User.objects.get(id=min.id)
        print(data1.share_price*int(noofshares))
        new=minn.invested-(data1.share_price*int(noofshares))
        print('1',new)
        if minn.invested>=(data1.share_price*int(noofshares)):
            Invest.objects.filter(id=id1.id).update(user_id=user.id,company_name_id=data1.id,noofsahes=noofshares)
            print('save')
            id.update(invested=new)
            messages.success(request,'details are updated')
            return redirect('list')
        messages.error(request,'u have a in sufficient amt')
        return redirect('list')
    qs=Company.objects.all()
    return render(request,"updateinvested.html",{'id':id1,'qs':qs})

@login_required(login_url='/user/')
def delete_investe(request,id):
    id=get_object_or_404(Invest,id=id)
    id.delete()
    messages.success(request,'delete successfully')
    return redirect('list')

def log_out_user(request):
    user=request.user
    if user:
        logout(request)
        messages.success(request,'logout successfully')
        return redirect('user')

