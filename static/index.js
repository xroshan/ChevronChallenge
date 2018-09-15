var app = new Vue({
  el: "#container",
  data: {
    user: "home",
    types: [],
    facilities: [],
    aLongitude:"",
    aLatitude:"",
    aWorkerName: "",
    aWorkerShift: "",
    aNewEquipmentType:""
  },
  mounted() {
    this.adminFiller();
  },
  methods: {
    //get equipmentType and list of facilities number
    adminFiller: function() {
      fetch("/api/equipment_type")
        .then(res => res.json())
        .then(data => {
          this.types = data;
        })
        .catch(err => console.error(err));

      fetch("api/facility")
        .then(res => res.json())
        .then(data => {
          this.facilities = data;
        })
        .catch(err => console.error(err));
    },

    //add new worker's name and shift
    addNewWorker: function() {
      fetch("/api/worker", {
        method: "post",
        body: JSON.stringify({
          'name': this.aWorkerName,
          'shift': this.aWorkerShift
        }),
        headers: {
          'Content-Type': 'application/json'
        }
      })
        .then(res => res.json())
        .then(data => {
          this.aWorkerName = "";
          this.aWorkerShift = "";
        })
        .catch(err => console.error(err));
    },

    //add facility latitude and longitude
    addNewFacility: function(){
      fetch("/api/facility",{
        method:"post",
        body: JSON.stringify({
          'lat':this.aLongitude,
          'lon':this.aLatitude
        }),
        headers:{
          'Content-Type':'application/json'
        }
      })
      .then(res=>res.json())
      .then(data=>{
        this.aLatitude="";
        this.aLongitude="";
      })
    },

    //add new equipment type
    addNewEquipmentType: function(){
      fetch("/api/equipment_type",{
        method:"post",
        body: JSON.stringify({
          'name':this.aNewEquipmentType
        }),
        headers:{
          'Content-Type':'application/json'
        }
      })
      .then(res=>res.json())
      .then(data=>{
        this.addNewEquipmentType="";
        this.adminFiller();
      })

    }
  } 
});
