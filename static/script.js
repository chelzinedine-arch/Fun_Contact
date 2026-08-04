document.addEventListener("DOMContentLoaded",function(){
const forms=document.querySelectorAll("form");
forms.forEach(function(form){
form.addEventListener("submit",function(event){
const required=form.querySelectorAll("[required]");
let valid=true;
required.forEach(function(input){
input.classList.remove("input-error");
if(input.value.trim()==""){
valid=false;
input.classList.add("input-error");
}
});
if(!valid){
event.preventDefault();
showNotification("Please fill all required fields.","error");}});});
const phones=document.querySelectorAll('input[name="phone"]');
phones.forEach(function(input){
input.addEventListener("input",function(){
this.value=this.value.replace(/[^0-9+ ]/g,"");});});
const deletes=document.querySelectorAll(".delete-button");
deletes.forEach(function(btn){
btn.addEventListener("click",function(e){
if(!confirm("Delete this contact ?")){
e.preventDefault();}});});
const search=document.querySelector(".search input");
if(search){
search.addEventListener("focus",function(){
this.classList.add("search-focus");});
search.addEventListener("blur",function(){
this.classList.remove("search-focus");});}
const rows=document.querySelectorAll("tbody tr");
rows.forEach(function(row,index){
row.style.opacity="0";
row.style.transform="translateY(20px)";
setTimeout(function(){
row.style.transition=".4s";
row.style.opacity="1";
row.style.transform="translateY(0)";},index*80);});
const message=document.querySelector(".message");
if(message){
setTimeout(function(){
message.style.opacity="0";},4000);}
window.showNotification=function(text,type="success"){
const old=document.querySelector(".js-notification");
if(old){old.remove();}
const note=document.createElement("div");
note.className="js-notification "+type;
note.textContent=text;
document.body.appendChild(note);
setTimeout(function(){
note.classList.add("show");},20);
setTimeout(function(){
note.classList.remove("show");
setTimeout(function(){
note.remove();},500);},3500);};
const topBtn=document.createElement("button");
topBtn.className="back-to-top";
topBtn.innerHTML="↑";
document.body.appendChild(topBtn);
window.addEventListener("scroll",function(){
if(window.scrollY>300){
topBtn.classList.add("show");}
else{
topBtn.classList.remove("show");
}
});
topBtn.addEventListener("click",function(){
window.scrollTo({
top:0,
behavior:"smooth"});});
forms.forEach(function(form){
form.addEventListener("submit",function(){
const btn=form.querySelector("button[type='submit']");
if(btn){
btn.disabled=true;
btn.innerHTML='<span class="spinner"></span>';}});});
window.addEventListener("load",function(){
document.body.classList.add("fade-in");});});
function toggleMenu(){
document.getElementById("mobileMenu").classList.toggle("show-menu");}
function togglePassword(id,eye){
const input=document.getElementById(id);
const icon=document.getElementById(eye);
if(input.type==="password"){
input.type="text";
icon.innerHTML="🙈";}
else{
input.type="password";
icon.innerHTML="👁️";}}
function previewImage(input,id){
if(input.files&&input.files[0]){
const reader=new FileReader();
reader.onload=function(e){
document.getElementById(id).src=e.target.result};
reader.readAsDataURL(input.files[0]);}}