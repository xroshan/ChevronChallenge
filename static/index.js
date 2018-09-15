fetch("/api/worker")
  .then(function (response){
    return response.json()
  })
  .then(function(worker){
    console.log('test data',worker)
  })

var app = new Vue({
  el: "#container",
  data: {
    user: "home",
    equipments:[
        {key:1, name: "Pump"},
        {key:2, name: "Compressor"},
        {key:3, name: "Seperator"},
        {key:4, name: "Sensor"},
        {key:5, name: "Security"},
        {key:6, name: "Electricity"},
        {key:7, name: "Networking"},
        {key:8, name: "Vehicle"},
        {key:9, name: "HVAC"},
        {key:10, name: "Conveyer"}
    ],
    aSelectedEquipment:1,
    facilities:[
        {key:1, name:"Facility 1"},
        {key:2, name:"Facility 2"},
        {key:3, name:"Facility 3"},
        {key:4, name:"Facility 4"},
        {key:5, name:"Facility 5"},
    ],
    aSelectedFacility:1
  }
});
