async function updateCart(food_id,action){
    console.log("action", food_id,action)
    const element = document.getElementById(`quantity-${food_id}`)
    console.log("elemmenr",element)
    let quantity = element.value
    quantity = parseInt(quantity)
    if(action == "increase"){
      await update_cart(food_id,action)
    }
    else if(action == "decrease"){
          if(quantity == 1){
            await update_cart(food_id,"remove")
          }
          else{
            await update_cart(food_id,"decrease")
          }
      }
    else{
          await update_cart(food_id,action)
      }
    }
  

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
  