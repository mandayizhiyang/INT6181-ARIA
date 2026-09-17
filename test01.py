def add_to_cart(item, cart=[]):
    cart.append(item)
    return cart
 
user1_cart = add_to_cart("Shoes")
user2_cart = add_to_cart("Hat")
 
print(f"User 2's cart: {user2_cart}")


# cart =[]
# def add_to_cart(item):
#     cart.append(item)
   
# add_to_cart("Shoes")
# add_to_cart("Hat")
# print(f"User 2's cart: {cart}")