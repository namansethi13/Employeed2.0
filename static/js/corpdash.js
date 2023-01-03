var where;


function inputskillsclicked(){
   where = document.getElementById("inputskills");
}

function inputcoursesclicked(){
   where = document.getElementById("inputcourses");
}

function inputtext(what){
   let str = "";
   what.forEach(element =>{
      where.setAttribute("value","");
      str += " "+element.innerHTML;
   })
   where.setAttribute("value",str);
}

class CustomSelect {

   constructor(originalSelect) {
      
      this.flag = 0;
      this.originalSelect = originalSelect;
      this.customSelect = document.createElement("div");
      this.customSelect.classList.add("select");
      this.selected = [];

      this.originalSelect.querySelectorAll("option").forEach((optionElement) => {
         
         const itemElement = document.createElement("div");
         itemElement.classList.add("select__item");
         itemElement.textContent = optionElement.textContent;
         this.customSelect.appendChild(itemElement);
         
         if(optionElement.selected){
            itemElement.classList.add("select__item--selected");
            this.selected.push(itemElement);
            inputtext(this.selected);
         }
         if(this.originalSelect.multiple && optionElement.classList.contains("select__item--selected")){
            this._select(itemElement);
         }
         itemElement.addEventListener("click", () => {
            
            if (
               this.originalSelect.multiple &&
               itemElement.classList.contains("select__item--selected")
            ) {
               this.indexel = this.selected.indexOf(optionElement);
               this.selected.splice(this.indexel,1);
               inputtext(this.selected);
               this._deselect(itemElement);
            } else {
               this.selected.push(optionElement);
               inputtext(this.selected);
               this._select(itemElement);
            }

         });
      });

      this.originalSelect.insertAdjacentElement("afterend", this.customSelect);
      this.originalSelect.style.display = "none";  //to hide orignal select option
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
   function Check(substring){
            url = String(window.location.href);
            let count = url.split(substring).length-1;
            return count;
         }
      if(Check("jobs/update/") > 0){

         if(selectElement.getAttribute("id") == "skills"){
               document.getElementById("skillsreq").click();
               setTimeout(function(){
                  document.getElementById("skillsclose").click();
               },1000);
            }
         if(selectElement.getAttribute("id") == "eligible_courses"){
               document.getElementById("eligiblecourses").click();
               setTimeout(function() {
                  document.getElementById("eligibilityclose").click();
               },1000);
         }
      }
   new CustomSelect(selectElement);
});

