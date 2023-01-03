// Changing Text of Download CSV Button upon resizing
if (window.innerWidth <= 992) {
   document.getElementById("downloadbtn").innerHTML = "Download";
}
else {
   document.getElementById("downloadbtn").innerHTML = "Download Sample CSV";
}
window.onresize = function (event) {
   if (window.innerWidth <= 992) {
      document.getElementById("downloadbtn").innerHTML = "Download";
   }
   else {
      document.getElementById("downloadbtn").innerHTML = "Download Sample CSV";
   }
}

function btnhide() {
   let orignalcourseoptions = document.getElementsByClassName("custom-select")[0].length;
   let courselist = document.querySelectorAll(".div1 p");
   console.log(orignalcourseoptions);
   if (courselist.length == orignalcourseoptions) {
      document.getElementById("addcoursebtn").setAttribute("disabled", "true");
      console.log("in");
   }
   else {
      console.log("inelse");
      document.getElementById("addcoursebtn").disabled = false;
   }
}


// Custom Select
class CustomSelect {
   constructor(originalSelect) {
      this.flag = 0;
      this.originalSelect = originalSelect;
      this.option = document.querySelectorAll('.div1 p');
      this.customSelect = document.createElement("div");
      this.customSelect.classList.add("select");

      btnhide();
      this.originalSelect.querySelectorAll("option").forEach((optionElement) => {

         const itemElement = document.createElement("div");
         itemElement.classList.add("select__item");
         itemElement.textContent = optionElement.textContent;
         this.customSelect.appendChild(itemElement);

         this.option.forEach(temp => {
            if (temp.innerHTML == optionElement.innerHTML) {
               this.flag = 1;
               return;
            }
         });

         if (this.flag == 1) {
            this.flag = 0;
            itemElement.classList.add("box");   // to hide the boxes
         }

         if (optionElement.selected) {
            this._select(itemElement);
         }


         itemElement.addEventListener("click", () => {
            if (
               this.originalSelect.multiple &&
               itemElement.classList.contains("select__item--selected")
            ) {
               this._deselect(itemElement);
            } else {
               this._select(itemElement);
            }

         });
      });

      this.originalSelect.insertAdjacentElement("afterend", this.customSelect);
      this.originalSelect.style.display = "none";
   }

   _select(itemElement) {
      const index = Array.from(this.customSelect.children).indexOf(itemElement);

      if (!this.originalSelect.multiple) {
         this.customSelect.querySelectorAll(".select__item").forEach((el) => {
            el.classList.remove("select__item--selected");
         });
      }

      this.originalSelect.querySelectorAll("option")[index].selected = true;
      itemElement.classList.add("select__item--selected");
   }

   _deselect(itemElement) {
      const index = Array.from(this.customSelect.children).indexOf(itemElement);

      this.originalSelect.querySelectorAll("option")[index].selected = false;
      itemElement.classList.remove("select__item--selected");
   }
}

document.querySelectorAll(".custom-select").forEach((selectElement) => {
   new CustomSelect(selectElement);
});



// Dynamic Modal for Confrim Delete Option

const confirmdelete = document.getElementById('confirmdelete');
if (confirmdelete != null) {
   confirmdelete.addEventListener('show.mdb.modal', (e) => {
      const button = e.relatedTarget;
      const course = button.getAttribute('data-mdb-whatever');
      const modalBodyInput = confirmdelete.querySelector('.modal-body p');

      modalBodyInput.classList.add("text-dark");
      modalBodyInput.innerHTML = "Are you sure you want to delete " + course + " course?";
   })
}

