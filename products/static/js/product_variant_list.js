
let previousSearchTerm = null;

document.addEventListener('DOMContentLoaded', async function () {
    const res = await updateProductVariantList();
  
    document.getElementById('search-input').addEventListener('keydown', async function (event) {
        if (event.key === 'Enter'){
            console.log("...enter pressed...")
            const searchTerm = event.target.value;
            console.log('...searchTerm...',searchTerm)
            event.target.value = `${searchTerm}`;
            if (searchTerm !== previousSearchTerm) {
                console.log("..keri")
                await updateProductVariantList(searchTerm);
                previousSearchTerm = searchTerm;
              }
        }
        
    });
  });


async function updateProductVariantList(searchTerm=null){
    try{
        const url = new URL('/api/product-variant/',window.location.origin);
        url.searchParams.append('page_size', 3);
        url.searchParams.append('page', 1);
        if (searchTerm) {
            url.searchParams.append('q', searchTerm);
          }
        console.log("................url...",url)
        const response = await fetch(url.toString());
        
        if (response.ok){
            console.log("....response//  ok")
            data = await response.json();
            console.log("/....data.....",data)
            data = data['results']
            console.log("/....data.....",data)
            productsContainer = document.getElementById('productsDiv')
            productsContainer.innerHTML = ""

            let content = `<div class="container my-5">
                            <div class="row">`
            data.forEach(function(product){
                let productCard = `
                                <div class="col-md-2 col-sm-6 mb-4">
                                    <a href="" class='product_link text-decoration-none text-dark' data-id=${product.id}>
                                        <div class="card h-100">
                                            <img src="${product.image1}" class="card-img-top h-75" style="object-fit:cover" alt="Product Image">
                                            <div class="card-body">
                                                <h5 class="card-title">${product.product.name}</h5>
                                                <p class="card-text" style="font-size:12px">${(product.description || product.product.description).slice(0,30) + "..."}</p>  
                                                <p class="card-text font-weight-bold">Rs. ${product.variant_price || product.product.price || ""}</p>
                                            </div>
                                        </div>
                                    </a>
                                </div>
                            
                        `
                content += productCard
            })
            productsContainer.innerHTML += content + `</div></div>`

            const productTiles = document.querySelectorAll('.product_link');
            
            productTiles.forEach(tile => {
                const productId = tile.getAttribute('data-id');
                tile.href = `/product/${productId}/`;
            });
            
            

        }
        else{
            console.log("Error")
        }
    }
    catch(error){
        console.log(error)
    }
}


