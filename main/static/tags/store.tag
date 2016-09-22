<category-list>
  <button class="btn btn-default btn-block {active:!window.PRODUCTS.c}" onclick={ reset }>
    Any Category</button>
  <button class="btn btn-default btn-block {active:window.PRODUCTS.c==category.pk}"
          onclick={ parent.click } each={ category,i in categories }>
    { category.name }</button>

  this.on("mount",function() {
    uR.ajax({
      url: "/shop/categories.js",
      success: function(data) {
        uR.drop.categories = data.categories;
        uR.drop.active_category = undefined;
      },
      that: this,
    });
  });

  click(e) {
    uR.drop.active_category = e.item && e.item.category && e.item.category.pk; 
    uR.drop.visible = 18;
    uR.drop.updateTags();
  }
</category-list>

<product-list>
  <div class="row">
    <product each={ product,i in products } product={ product } class={ parent.className }></product>
    <product-admin each={ product,i in admin_products } product={ product } class="col-sm-6 col-md-4"></product-admin>
  </div>
  <button class="btn btn-warning btn-block" onclick={ more } if={uR.drop.visible<this.max_products}>
    Load More</button>

  var self = this;
  this.on("mount",function() {
    this.className = this.opts.className || "col-sm-6 col-md-4";
    this.update();
  });
  this.on("update",function() {
    this.products = uR.drop.products_list;
    if (!this.products) { return }
    if (uR.drop.active_category) {
      this.products = this.products.filter(function(p){
        return p.categories.indexOf(uR.drop.active_category) != -1;
      });
    }
    if (this.opts.ids) {
      this.products = this.products.filter(function(p) { return self.opts.ids.indexOf(p.pk) !=-1 })
    }
    this.max_products = this.products.length;
    this.products = this.products.slice(0,uR.drop.visible);
    if (this.products.extra) {
      this.admin_products = this.products;
      this.products = [];
    }
  });
  more(e) {
    uR.drop.visible += 12;
  }
</product-list>

<product>
  <div class="well {incart:product.quantity,out-of-stock:product.in_stock==0,hidden:dat}">
    <div class="img" style="background-image: url({ product.thumbnail })"></div>
    <div class="bottom">
      <div class="name">{ product.name }</div>
      <div class="row">
        <div class="col-xs-{ product.quantity?12:6 } price">
          ${product.unit_price}
          <span if={ product.quantity }>x { product.quantity }</span>
        </div>
        <div class="col-xs-6" if={ !product.quantity }>
          <button class="btn btn-success btn-block" onclick={ plusOne }>Add to Cart</button>
        </div>
      </div>
      <div class="row cart-buttons">
        <div class="col-xs-3">
          <button class="btn btn-success btn-block" onclick={ plusOne }>+1</button>
        </div>
        <div class="col-xs-3">
          <button class="btn btn-danger btn-block" onclick={ minusOne }>-1</button>
        </div>
        <div class="col-xs-6">
          <button class="btn btn-primary btn-block" onclick={ uR.drop.openCart }>Checkout</button>
        </div>
      </div>
    </div>
  </div>

  var update_timeout;
  var self = this;
  self.product = opts.product;
  this.product.quantity = this.product.quantity || 0;
  function updateCart() {
    clearTimeout(update_timeout);
    update_timeout = setTimeout(_updateCart,100);
  }
  this.on("update",function() { console.log(1); });
  function _updateCart() {
    uR.forEach(uR.drop.cart.all_items,function(c) {
      if (c.product_id = self.product.id) { c.quantity = self.product.quantity; }
    });
    uR.drop.ajax({
      url: '/edit/',
      method: "POST",
      data: {pk: self.product.id,quantity: self.product.quantity}
    });
  }
  plusOne(e) {
    self.product.quantity++;
    updateCart();
  }
  minusOne(e) {
    self.product.quantity--;
    updateCart();
  }
</product>

<product-admin>
  <div class="well">
    <div class="img {out-of-stock:product.in_stock==0}">
      <img src={ product.img.url } />
    </div>
    <div class="name">{ product.name }</div>
    <div class="price">
      ${ product.price }
      <span class="pull-right">In Stock: { product.in_stock||"null" }</span>
    </div>
    <div class="row">
      <div class="col-xs-6">
        <a href="/admin/store/consumable/{ product.pk }/" class="fa fa-pencil-square btn btn-primary btn-block">
          Edit</a>
      </div>
      <div class="col-xs-6">
        <a href="{ product.purchase_url }" class="btn btn-info btn-block {hidden:!product.purchase_url}">
          <i class="fa fa-shopping-cart"></i> { product.purchase_domain }</a>
      </div>
    </div>
    <div class="flexy">
      <button onclick={ add1 } class="btn btn-success" if={ product.purchase_quantity != 1 }>
        +1</button>
      <button onclick={ subtract1 } class="btn btn-danger" if={ product.purchase_quantity != 1 }>
        -1</button>
      <button onclick={ add } class="btn btn-success">
        +{ product.purchase_quantity }</button>
      <button onclick={ subtract } class="btn btn-danger">
        -{ product.purchase_quantity }</button>
    </div>
  </div>

  var self = this;
  self.product = this.opts.product;
  function modify(quantity) {
    $.post(
      '/shop/admin/add/',
      {quantity:quantity,pk:self.product.pk},
      function(data) {
        self.product.in_stock = data;
        self.update();
      }
    )
  }
  add1(e) {
    modify(1);
  }
  subtract1(e) {
    modify(-1);
  }
  add(e) {
    modify(e.item.product.purchase_quantity);
  }
  subtract(e) {
    modify(-e.item.product.purcase_quantity);
  }
</product-admin>
