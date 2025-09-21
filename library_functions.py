import os
from supabase import create_client, Client  # pip install supabase
from dotenv import load_dotenv  # pip install python-dotenv
from datetime import datetime, timedelta

load_dotenv()

# Get environment variables
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

# Create Supabase client
sb: Client = create_client(url, key)


# ------------------ CREATE ------------------ #
def add_members(id,name,email,join_date):
    payload = {"member_id":id,"name":name,"email":email,"join_date":join_date}
    resp = sb.table("members").insert(payload).execute()
    return resp.data
def add_books(id,title,author,category,stock):
    payload = {"book_id":id,"title":title,"author":author,"category":category,"stock":stock}
    resp = sb.table("books").insert(payload).execute()
    return resp.data


# ------------------ READ ------------------ #
def display():
    resp=sb.table("members").select("*").execute()
    return resp.data
def available_books():
    resp=sb.table("books").select("title,stock").execute()
    resp=resp.data
    if(resp):
        print("available books are:")
        for row in resp:
            if(row["stock"]>0):
                print(row["title"])
    else:
        print("No available books")
def search(s):
    resp=sb.table("books").select("title,author,category").execute()
    resp=resp.data
    flag=False
    if(resp):
        for row in resp:
            if(s==row["title"] or s==row["author"] or s==row["category"]):
                flag=True
                break
                print("Book found")
        if(flag):
            print("Book found")
        else:
            print("No Book found")
    else:
        print("No available books")


def member_details(member_id):
    member = sb.table("members").select("*").eq("member_id", member_id).execute().data
    borrowed = sb.table("borrow_records").select("book_id, borrow_date, return_date").eq("member_id", member_id).execute().data
    return {"member": member, "borrowed_books": borrowed}


# ------------------ UPDATE ------------------ #
def update_book(title,copies):
    resp=sb.table("books").update({"stock":copies}).eq("title",title).execute()
    return resp.data
def update_member(name,email):
    resp=sb.table("members").update({"email":email}).eq("name",name).execute()
    return resp.data


# ------------------ DELETE ------------------ #
def delete_member(member_id):
    # check if member has any unreturned books
    borrowed = (
        sb.table("borrow_records")
        .select("*")
        .eq("member_id", member_id)
        .is_("return_date", None)   # correct way to check NULL
        .execute()
        .data
    )
    if borrowed:
        return "Member still has borrowed books!"

    # delete member
    resp = (
        sb.table("members")
        .delete()
        .eq("member_id", member_id) 
        .execute()
    )
    return resp.data



def delete_book(book_id):
    # check if book is currently borrowed
    borrowed = (
        sb.table("borrow_records")
        .select("*")
        .eq("book_id", book_id)
        .is_("return_date", None)
        .execute()
        .data
    )
    if borrowed:
        return "Book is still borrowed!"

    # delete borrow history first
    sb.table("borrow_records").delete().eq("book_id", book_id).execute()

    # now delete book
    resp = sb.table("books").delete().eq("book_id", book_id).execute()
    return resp.data


# ------------------ BORROW (Transaction) ------------------ #
def borrow_book(member_id, book_id):
    book = sb.table("books").select("stock").eq("book_id", book_id).execute().data
    if not book or book[0]["stock"] <= 0:
        return "Book not available"

    try:
        # 1. Decrease stock
        sb.table("books").update({"stock": book[0]["stock"] - 1}).eq("book_id", book_id).execute()

        # 2. Insert borrow record
        borrow_data = {"member_id": member_id, "book_id": book_id, "borrow_date": datetime.now().isoformat()}
        sb.table("borrow_records").insert(borrow_data).execute()

        return "Borrow successful"
    except Exception as e:
        return f"Transaction failed: {str(e)}"


# ------------------ RETURN (Transaction) ------------------ #
from datetime import datetime

def return_book(member_id, book_id):
    try:
        # 1. Update borrow record
        sb.table("borrow_records").update({
            "return_date": datetime.now().isoformat()
        }).eq("member_id", member_id)\
          .eq("book_id", book_id)\
          .is_("return_date", None)\
          .execute()

        # 2. Increase stock
        book = sb.table("books").select("stock").eq("book_id", book_id).execute().data
        sb.table("books").update({"stock": book[0]["stock"] + 1}).eq("book_id", book_id).execute()

        return "Return successful"
    except Exception as e:
        return f"Transaction failed: {str(e)}"



# ------------------ REPORTS ------------------ #

def overdue_books():
    cutoff = datetime.now() - timedelta(days=14)
    resp = sb.table("borrow_records").select("member_id, book_id, borrow_date").is_("return_date", None).lt("borrow_date", cutoff.isoformat()).execute()
    return resp.data


# ------------------ MAIN TEST ------------------ #
if __name__ == "__main__":
    # print(display_members())
    # available_books()
    # print(borrow_book(1, 101))   # Example: Member 1 borrows Book 101
    # print(return_book(1, 101))   # Example: Member 1 returns Book 101
    print(borrow_book(5,1))
