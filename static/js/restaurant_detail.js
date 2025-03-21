document.addEventListener("DOMContentLoaded", function () {
    // Select all buttons with the class 'add-to-cart'
    const buttons = document.querySelectorAll(".add-to-cart");

    buttons.forEach(button => {
        button.addEventListener("click", async function () {
            const productId = this.getAttribute("data-id");  // Get product ID
            addToCart(productId,this);  // Call async function
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


function updateCart(food_id,action){
  console.log("action",typeof food_id,action)
  const element = document.getElementById(`quantity-${food_id}`)
  let quantity = element.innerText
  quantity = parseInt(quantity)
  if(action == "increase"){
    quantity+=1
    element.innerText = quantity
  }
  else{
    if(quantity == 1){
        console.log("hide")
    }
    else{
        quantity -=1
        element.innerText = quantity
    }
  }
  console.log(typeof quantity)
}
