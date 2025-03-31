document.addEventListener("DOMContentLoaded", function () {
    
    const buttons = document.querySelectorAll(".add-to-cart");

    buttons.forEach(button => {
        button.addEventListener("click", async function () {
            const productId = this.getAttribute("data-id");  
            addToCart(productId,this);  
        });
    });
});

async function addToCart(productId,button){
    console.log("product id",productId)
    const url = "/order/add-to-cart"
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    const requestBody = {
        method:"POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken, 
        },
        body: JSON.stringify({ product_id: productId })
    }

    const response = await fetch(url,requestBody)
    console.log("res",response.status)
    if(response.status == 200){
        const responseData = await response.json()
        console.log("res",responseData)
        button.style.display = "none"
        document.getElementById(`cart-button-${productId}`).style.display="flex"
        return 200
    }
    else if(response.status == 400){
        Swal.fire({
            title: "Login Required",
            text: "Please Sign In",
            icon: "warning",
            confirmButtonText: "Go to Sign In"
          }).then(() => {
            navigate('/login');
          });
    }
    }


async function updateCart(food_id,action){
  console.log("action",typeof food_id,action)
  const element = document.getElementById(`quantity-${food_id}`)
  let quantity = element.innerText
  quantity = parseInt(quantity)
  if(action == "increase"){
    await update_cart(food_id,action)
    // quantity+=1
    // element.innerText = quantity
  }
  else{
    if(quantity == 1){
        await update_cart(food_id,"remove")
    }
    else{
        await update_cart(food_id,"decrease")
    }
  }
  console.log(typeof quantity)
}

// async function updateCart(food_id,action){
//     console.log("action", food_id,action)
//     const element = document.getElementById(`quantity-${food_id}`)
//     console.log("elemmenr",element)
//     let quantity = element.value
//     quantity = parseInt(quantity)
//     if(action == "increase"){
//       await update_cart(food_id,action)
//     }
//     else if(action == "decrease"){
//           if(quantity == 1){
//             await update_cart(food_id,"remove")
//           }
//           else{
//             await update_cart(food_id,"decrease")
//           }
//       }
//     else{
//           await update_cart(food_id,action)
//       }
//     }

async function update_cart(food_id,action){
        const url = "/order/update/cart"
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    
        const requestBody = {
            method:"POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken, 
            },
            body: JSON.stringify({ product_id: food_id,action:action })
        }
    
        const response = await fetch(url,requestBody)
        if (response.status == 200){
            const response_data = await response.json()
            console.log(response_data)
            location.reload()
        } 
    }