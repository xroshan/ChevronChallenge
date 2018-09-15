const DropDown = Vue.component("dropdown", {
    template: "#dropdown",
    data() {
      return {
        showDropDown: true,
        links: [
          {
            name: "Account"
          },
          {
            name: "Profile"
          },
          {
            name: "Logout"
          }
        ]
      };
    }
  });

var app = new Vue({
    el: '#container',
    data:{
        user:'home'
    }
})

