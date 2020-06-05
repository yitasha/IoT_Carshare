//Select box filter
function filterPrice() {
    // Declare variables
    var input, filter, table, tr, td, i, cellValue;
    input = document.getElementById("filterText");
    filter = parseInt(input.value);
    table = document.getElementById("carTable");
    tr = table.getElementsByTagName("tr");
  
    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[7];
      if (td) {
        cellValue = parseInt(td.innerHTML);
        if (cellValue <= filter) {
            tr[i].style.display = "";
        } else {
            tr[i].style.display = "none";
        }
      }
    }
}

//Search filter cars
$(document).ready(function(){
    $("#myInput").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#carsTable tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});

//Search filter for users
$(document).ready(function(){
    $("#userInput").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#userTable tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});