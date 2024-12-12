document.addEventListener("DOMContentLoaded", function(event){
    event.preventDefault();
    
    const pathParts = window.location.pathname.split('/')
    const productVariantId = pathParts[pathParts.length - 1] || pathParts[pathParts.length - 2]

    const mainDiv = document.getElementById('mainDiv');
    mainDiv.classList.add('card');

    getProductDetails(productVariantId)

    
})


async function getProductDetails(productVariantId){
    try{
        const response = await fetch(`/api/product-variant/${productVariantId}/`)
        const sizesDiv = document.getElementById('sizesAvailable')
        const stockAvailableDiv = document.getElementById('availableStocksDiv')
        sizesDiv.innerHTML = ""

        if (response.ok) {
            product = await response.json();
            document.getElementById("productImage").src = product.image1;
            document.getElementById("productName").textContent = product.product.name;
            document.getElementById("productPrice").textContent = `Rs. ${product.variant_price || product.product.price}`;
            document.getElementById("productDescription").textContent = product.description || product.product.description;
            if (!product.quantity){
                stockAvailableDiv.innerHTML = `Currently out of stock`
                stockAvailableDiv.classList.add("text-muted")
                stockAvailableDiv.style.fontWeight = "normal"
            }
            else if (product.quantity<=5){
                stockAvailableDiv.innerHTML = `Only ${product.quantity} left in stock`
                stockAvailableDiv.classList.add('text-danger')
                
            }
            const sizes_data = await getSizesAvailable(product.product.group_sku_number, product.color)
            console.log("...sizes_data.....",sizes_data)
            if(sizes_data){
                console.log("...buttoning..")
                sizes_data.forEach(data => {
                    console.log(data,"...data")
                    console.log(data.size,"...data")
                    sizesDiv.innerHTML += `<button id='btn-${data.size}' data-product-variant-id='${data.id}' onclick="changeSize(event)" class="btn btn-outline-primary m-2">${data.size}</button>`
                })
                document.getElementById(`btn-${product.size}`).classList.add('btn-primary', 'text-light');
            }
        }

        else {
            console.error("Failed to load product data.");
        }
    }
    catch(error){
        console.log(error)
    }

}

async function changeSize(event){
    console.log("..size cahnging..")
    const currentSizeBtn = document.getElementById('sizesAvailable').querySelector('.btn-primary.text-light')
    const clickedSizeBtn = event.target; 
    if(currentSizeBtn){
        currentSizeBtn.classList.remove('btn-primary','text-light');
    }
    clickedSizeBtn.classList.add('btn-primary', 'text-light');
    const targetSize = clickedSizeBtn.innerText;
    const target_product_variant_id = clickedSizeBtn.getAttribute('data-product-variant-id')
    console.log(target_product_variant_id,"...target_product_variant_id...")
    const productvariantDetails = getProductDetails(target_product_variant_id)
    if(productvariantDetails)
        window.location.href = `/product/${target_product_variant_id}/`
    
}




async function getSizesAvailable(groupSkuNumber, productColor) {
    try {
        const response = await fetch(`/api/product-sizes/${groupSkuNumber}/${productColor}/`);
        if (response.ok) {
            const data = await response.json();
            console.log(data,"....datataii..")
            return data;
        } else {
            console.error("Failed to fetch available sizes");
            return [];
        }
    } catch (error) {
        console.error("Error fetching sizes:", error);
        return [];
    }
}

// async function getAvailableStockCount(productVariantId){
//     const response = await fetch(`/api/product-variant/${productVariantId}/count/`);
//     const availableStocksDiv = document.get
// }


