// Dynamic Order Options Based On Field Selected
const fieldselect = document.getElementById("fieldselect");
const orderselect = document.getElementById("orderselect");

const intoptions = document.querySelectorAll(".integer");
const stringoptions = document.querySelectorAll(".string");

fieldselect.addEventListener('change', function () {
   orderselect.selectedIndex = 0;   // to reset value to not selected
   switch (fieldselect.options[fieldselect.selectedIndex].innerHTML) {
      case "#":
      case "Enroll Number":
      case "Age":
         for (i = 0, j = 0; i < stringoptions.length && j < intoptions.length; i++, j++) {
            stringoptions[i].setAttribute('hidden', 'hidden');
            intoptions[i].removeAttribute('hidden');
         }
         break;
      case "Email":
      case "Username":
         for (i = 0, j = 0; i < intoptions.length && j < stringoptions.length; i++, j++) {
            stringoptions[i].removeAttribute('hidden');
            intoptions[i].setAttribute('hidden', 'hidden');
         }

         break;
   }
})

// Sorting
function sortTable() {
   // Field to be Sorted
   const field = fieldselect.options[fieldselect.selectedIndex];
   // In Order
   const order = orderselect.options[orderselect.selectedIndex].innerHTML;
   // Type of order
   const ordertype = orderselect.options[orderselect.selectedIndex].attributes.class.textContent;

   // Sortin if it is an integer field
   if ((ordertype.toLowerCase()) == "integer") {

      var table;
      table = document.getElementById("table");
      var rows, i, x, y, count = 0;
      var switching = true;
      // Run loop until no switching is needed
      while (switching) {
         switching = false;
         var rows = table.rows;
         //Loop to go through all rows
         for (i = 1; i < (rows.length - 1); i++) {
            var Switch = false;

            // Fetch 2 elements that need to be compared
            x = rows[i].getElementsByTagName("TD")[field.value-1];
            y = rows[i + 1].getElementsByTagName("TD")[field.value-1];

            // Check the direction of order
            if (order.toLowerCase() == "ascending") {

               // Check if 2 rows need to be switched
               if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                  // If yes, mark Switch as needed and break loop
                  Switch = true;
                  break;
               }
            } else if (order.toLowerCase() == "descending") {

               if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                  // If yes, mark Switch as needed and break loop
                  Switch = true;
                  break;
               }
            }
         }
         if (Switch) {
            // Function to switch rows and mark switch as completed
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;

            // Increase count for each switch
            count++;
         } else {
            if (count == 0 && order.toLowerCase() == "ascending") {
               order = "descending";
               switching = true;
            }
         }
      }
   }
   // Sorting if it is an String Field
   if ((ordertype.toLowerCase()) == "string") {

      var table, i, x, y;
      table = document.getElementById("table");
      var switching = true;

      // Run loop until no switching is needed
      while (switching) {
         switching = false;
         var rows = table.rows;

         // Loop to go through all rows
         for (i = 1; i < (rows.length - 1); i++) {
            var Switch = false;

            // Fetch 2 elements that need to be compared
            x = rows[i].getElementsByTagName("TD")[0];
            console.log(x);
            y = rows[i + 1].getElementsByTagName("TD")[0];
            console.log(y);

            // Check if 2 rows need to be switched
            if (order == "(A to Z) Alphabetical") {
               if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {

                  // If yes, mark Switch as needed and break loop
                  Switch = true;
                  break;
               }
            }
            else if (order == "(Z to A) Alphabetical")
            {
               if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                  // If yes, mark Switch as needed and break loop
                  Switch = true;
                  break;
               }
            }
         }
         if (Switch) {
            // Function to switch rows and mark switch as completed
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
         }
      }
   }
}