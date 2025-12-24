from flask import Flask, request, render_template_string, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

env = os.getenv("ENV", "development")
if env == "production":

    os.environ["OPENAI_API_KEY"] = "your_production_api_key_here"

api_key = os.getenv("OPENAI_API_KEY")
if not api_key or api_key == "your_openai_api_key_here":
    client = None
else:
    client = OpenAI(api_key=api_key)

app = Flask(__name__)
CORS(app)

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Product Writer</title>

<style>

#tool{
    display:none;
}

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

*{box-sizing:border-box}
body{
    margin:0;
    font-family:'Inter',sans-serif;
    background:radial-gradient(circle at top left,#7f7cff,#1f1c2c);
    color:#fff;
    scroll-behavior:smooth;
}

/* HEADER */
header{
    position:fixed;
    top:0;
    width:100%;
    z-index:100;
    background:rgba(20,20,40,.75);
    backdrop-filter:blur(14px);
}
.nav{
    max-width:1100px;
    margin:auto;
    padding:14px 20px;
    display:flex;
    justify-content:space-between;
    align-items:center;
}
.logo{font-weight:700;font-size:18px}
.nav a{
    margin-left:18px;
    color:#fff;
    text-decoration:none;
    font-size:14px;
    opacity:.85;
}
.nav a:hover{opacity:1;color:#c7c6ff}

/* 3 DOT MENU */
.menu-wrapper{position:relative}
.three-dot{
    font-size:22px;
    cursor:pointer;
    margin-left:20px;
}
.menu-box{
    position:absolute;
    right:0;
    top:32px;
    background:rgba(30,30,60,.95);
    border-radius:12px;
    width:180px;
    display:none;
    overflow:hidden;
}
.menu-box div{
    padding:12px 16px;
    cursor:pointer;
    font-size:14px;
}
.menu-box div:hover{
    background:rgba(255,255,255,.15);
}

/* SECTIONS */
section{padding:120px 20px;max-width:1100px;margin:auto}

/* HOME */
.home h1{font-size:38px;text-align:center}
.home p{text-align:center;max-width:700px;margin:auto;opacity:.85}
.features{
    margin-top:40px;
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(220px,1fr));
    gap:20px;
}
.feature{
    background:rgba(255,255,255,.12);
    padding:20px;
    border-radius:16px;
}


/* HOW */
.steps{margin-top:30px;display:grid;gap:20px}
.step{
    background:rgba(255,255,255,.12);
    padding:20px;
    border-radius:16px;
}

/* START */
.start-box{
    background:rgba(255,255,255,.12);
    padding:30px;
    border-radius:20px;
    text-align:center;
}
.start-box button{
    margin-top:15px;
    width:100%;
    padding:14px;
    border:none;
    border-radius:12px;
    font-size:16px;
    cursor:pointer;
    background:linear-gradient(135deg,#8f94fb,#4e54c8);
    color:#fff;
}
.skip{background:transparent;border:1px solid rgba(255,255,255,.4)}

/* TOOL */
.container{
    max-width:420px;
    margin:auto;
    padding:35px;
    border-radius:20px;
    background:rgba(255,255,255,.12);
    backdrop-filter:blur(18px);
}
.form-group{position:relative}
.form-group input{
    width:100%;
    padding:14px;
    border-radius:10px;
    border:1px solid rgba(255,255,255,.35);
    background:transparent;
    color:#fff;
}
button.generate{
    width:100%;
    margin-top:25px;
    padding:14px;
    border-radius:12px;
    border:none;
    font-size:16px;
    cursor:pointer;
    background:linear-gradient(135deg,#8f94fb,#4e54c8);
    color:#fff;
}
#result{
    margin-top:25px;
    padding:16px;
    border-radius:14px;
    background:rgba(255,255,255,.15);
    position:relative;   /* 👈 add */
}

.copy-btn{
    position:absolute;
    top:10px;
    right:10px;
    cursor:pointer;
    font-size:18px;
    opacity:0.8;
}
.copy-btn:hover{
    opacity:1;
}


/* SUGGESTIONS */
.suggestions{
    position:absolute;
    top:50px;
    width:100%;
    background:rgba(30,30,60,.95);
    border-radius:10px;
    display:none;
}
.suggestions div{
    padding:10px 14px;
    cursor:pointer;
}
.suggestions div:hover{
    background:rgba(255,255,255,.15);
}

/* HISTORY MODAL */
.modal{
    position:fixed;
    inset:0;
    background:rgba(0,0,0,.65);
    display:none;
    justify-content:center;
    align-items:center;
}
.modal-box{
    background:#1f1c2c;
    padding:25px;
    border-radius:16px;
    width:90%;
    max-width:420px;
    max-height:70vh;
    overflow:auto;
}
.history-item{
    background:rgba(255,255,255,.12);
    padding:12px;
    border-radius:10px;
    margin-bottom:10px;
    font-size:13px;
}
</style>
</head>

<body>

<header>
    <div class="nav">
        <div class="logo">✨ Listify AI</div>

        <div style="display:flex;align-items:center">
            <a href="#home">Home</a>
            <a href="#how">How it works</a>
            <a href="#start">Start</a>
            <a href="#tool">Tool</a>

            <div class="menu-wrapper">
                <span class="three-dot" onclick="toggleMenu()">⋮</span>
                <div class="menu-box" id="menuBox">
                    <div onclick="openHistory()">📜 History</div>
                </div>
            </div>
        </div>
    </div>
</header>

<!-- HOME -->
<section id="home" class="home">
    <h1>AI Product Description Generator</h1>

    <p>
        આ AI Product Description Generator એક smart web tool છે જે
        Artificial Intelligence નો ઉપયોગ કરીને કોઈપણ product માટે
        professional, attractive અને sales-focused description બનાવે છે.
    </p>

    <p style="margin-top:14px">
        Ecommerce sellers, small business owners, digital marketers અને
        students માટે આ tool ખૂબ જ ઉપયોગી છે. Amazon, Flipkart, Meesho,
        Shopify, Instagram ads અને websites માટે ready-to-use content
        seconds માં generate થાય છે.
    </p>

    <p style="margin-top:14px">
        તમને copywriting, marketing કે English writing આવડતું ન હોય
        તો પણ કોઈ problem નથી. ફક્ત product name લખો અને AI
        automatically features, benefits અને usage મુજબ description તૈયાર કરે છે.
    </p>

    <div class="features">
        <div class="feature">⚡ Seconds માં description generate</div>
        <div class="feature">🤖 AI powered human-like writing</div>
        <div class="feature">🛍 Any product category supported</div>
        <div class="feature">✨ Clean, readable & copy-ready content</div>
    </div>
</section>


<!-- HOW -->
<section id="how">
    <h2>How It Works</h2>

    <p style="max-width:720px;opacity:.85">
        આ tool advanced AI language model પર આધારિત છે જે natural language
        સમજે છે અને product related meaningful content generate કરે છે.
        User ને કોઈ technical knowledge ની જરૂર નથી.
    </p>

    <div class="steps">
        <div class="step">
            1️⃣ <strong>Product Name દાખલ કરો</strong><br>
            જેમ કે: Cotton Shirt, Smart Watch, Mobile Phone
        </div>

        <div class="step">
            2️⃣ <strong>AI Product Analyze કરે</strong><br>
            Product category, common features અને customer needs સમજે છે
        </div>

        <div class="step">
            3️⃣ <strong>Description Generate થાય</strong><br>
            Title, short introduction અને bullet-points સાથે
        </div>

        <div class="step">
            4️⃣ <strong>Instant Copy & Use</strong><br>
            Generate થતા જ description copy થઈ જાય છે
        </div>
    </div>
</section>


<!-- START -->
<section id="start">
    <h2>Get Started</h2>

    <div class="start-box">
        <p>
            તમારું email નાખીને direct login કરો
            અને tool નો ઉપયોગ શરૂ કરો.
        </p>

        <input
            id="loginEmail"
            type="email"
            placeholder="Enter your email"
            style="
                width:100%;
                padding:14px;
                border-radius:10px;
                border:1px solid rgba(255,255,255,.35);
                background:transparent;
                color:#fff;
                margin-top:12px;
            "
        >

        <button onclick="emailLogin()">Login & Continue</button>
        <button class="skip" onclick="skipLogin()">Skip</button>


        <p style="margin-top:10px;opacity:.7">
            (No password required)
        </p>
    </div>
</section>



<!-- TOOL -->
<section id="tool">
    <div class="container">
        <h2>Generate Description</h2>
        <form method="post">
            <div class="form-group">
                <input id="productInput" name="product" placeholder="Start typing product" autocomplete="off" required>
                <div class="suggestions" id="suggestions"></div>
            </div>
            <button class="generate" type="submit">Generate</button>
        </form>
        <div id="result">
    <span class="copy-btn" onclick="copyText()" title="Copy">📋</span>
</div>

    </div>
</section>

<!-- HISTORY MODAL -->
<div class="modal" id="historyModal">
    <div class="modal-box">
        <h3>Generated History</h3>
        <div id="historyList"></div>
        <button class="generate" onclick="closeHistory()">Close</button>
    </div>
</div>

<script>

function scrollToTool(){
    const tool = document.getElementById("tool");
    tool.style.display = "block";
    tool.scrollIntoView({ behavior: "smooth" });
}
function skipLogin(){
    // Go to home section
    document.getElementById("home").scrollIntoView({ behavior: "smooth" });
}


/* HISTORY STORAGE */
let historyData = [];

/* MENU */
function toggleMenu(){
    const m=document.getElementById("menuBox");
    m.style.display = m.style.display==="block"?"none":"block";
}

/* HISTORY */
function openHistory(){
    toggleMenu();
    const modal=document.getElementById("historyModal");
    const list=document.getElementById("historyList");
    list.innerHTML = historyData.length
        ? historyData.map(h=>`<div class="history-item">${h}</div>`).join("")
        : "<p>No history yet</p>";
    modal.style.display="flex";
}
function closeHistory(){
    document.getElementById("historyModal").style.display="none";
}

/* SUGGESTIONS */
/* SUGGESTIONS */
const products = [
  // Fashion
  "Shirt","T-Shirt","Jeans","Shoes","Sneakers","Sandals","Kurti","Saree",
  "Jacket","Hoodie","Cap","Belt","Wallet",

  // Electronics
  "Mobile Phone","Smartphone","Laptop","Gaming Laptop","Tablet","Smart Watch",
  "Bluetooth Earbuds","Headphones","Speaker","Power Bank","Charger","USB Cable",
  "Smart TV","LED TV","Camera","Tripod",

  // Home & Kitchen
  "Mixer Grinder","Pressure Cooker","Water Bottle","Lunch Box",
  "Electric Kettle","Induction Cooktop","Refrigerator",
  "Washing Machine","Microwave Oven","Air Fryer",

  // Beauty & Personal Care
  "Face Wash","Moisturizer","Body Lotion","Perfume","Hair Oil",
  "Shampoo","Conditioner","Beard Trimmer","Hair Dryer",

  // Grocery
  "Rice","Wheat Flour","Sugar","Tea","Coffee","Cooking Oil","Spices",

  // Sports
  "Cricket Bat","Football","Badminton Racket","Yoga Mat","Dumbbells",

  // Office & Travel
  "Notebook","Pen","Office Chair","Study Table",
  "Backpack","Travel Bag","Suitcase"
];

const input=document.getElementById("productInput");
const box=document.getElementById("suggestions");

input.addEventListener("input", () => {
    const v = input.value.toLowerCase().trim();
    box.innerHTML = "";

    if (!v) {
        box.style.display = "none";
        return;
    }

    products
        .filter(p => p.toLowerCase().includes(v))
        .slice(0, 8)   // max 8 suggestions
        .forEach(p => {
            const d = document.createElement("div");
            d.textContent = p;
            d.onclick = () => {
                input.value = p;
                box.style.display = "none";
            };
            box.appendChild(d);
        });

    box.style.display = "block";
});


/* FORM */
document.querySelector("form").addEventListener("submit",async e=>{
    e.preventDefault();
    result.innerHTML="⏳ Generating...";
    const fd=new FormData(e.target);
    const r=await fetch("/",{method:"POST",body:fd,headers:{'X-Requested-With':'XMLHttpRequest'}});
    const d=await r.json();
   result.innerHTML = `<span class="copy-btn" onclick="copyText()">📋</span>` + d.result;

    historyData.unshift(d.result);
});

function copyText(){
    const resultBox = document.getElementById("result");
    const text = resultBox.innerText.replace("📋","").trim();

    if(!text){
        alert("❌ Nothing to copy");
        return;
    }

    navigator.clipboard.writeText(text);
    alert("✅ Description copied");
}


function emailLogin(){
    const email = document.getElementById("loginEmail").value.trim();

    if(!email){
        alert("❌ Please enter email");
        return;
    }

    if(!email.includes("@")){
        alert("❌ Invalid email");
        return;
    }

    // Save user (frontend only)
    localStorage.setItem("user", JSON.stringify({ email }));

    alert("✅ Logged in as " + email);

    // Continue to tool
    scrollToTool();
}
function copyText(){
    const resultBox = document.getElementById("result");
    const text = resultBox.innerText.replace("📋","").trim();

    if(!text){
        alert("❌ Nothing to copy");
        return;
    }

    navigator.clipboard.writeText(text);
    alert("✅ Description copied");
}






</script>

</body>
</html>
"""




@app.route("/", methods=["GET","POST"])
def home():
    result=""
    if request.method=="POST":
        p = request.form["product"]
        if not client:
            result = "Please set your OpenAI API key in the .env file"
        else:
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role":"user","content":f"Write a concise, engaging product description for '{p}'. Include: title, brief intro, 3-5 key features in bullets, benefits, sizes, care. Keep it under 50 words."}
                    ],
                    max_tokens=400,
                    temperature=0.7
                )
                result = response.choices[0].message.content
                # Format for readability
                result = result.replace('\n', '<br>').replace('**', '<strong>', 1).replace('**', '</strong>', 1)
                # Handle multiple **
                import re
                result = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', result)
            except Exception as e:
                result = f"Error generating description: {str(e)}"
        
        return jsonify({'result': result})
    return render_template_string(HTML, result=result)

app.run(debug=True)