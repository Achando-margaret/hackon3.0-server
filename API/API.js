// server.js
import express from "express";
import bodyParser from "body-parser";
import Stripe from "stripe";
import axios from "axios";

const app = express();
app.use(bodyParser.json());

// 🔹 Stripe Setup
const stripe = new Stripe("STRIPE_SECRET_KEY");

// 🔹 M-Pesa Setup
const mpesaConfig = {
  consumerKey: "YOUR_MPESA_CONSUMER_KEY",
  consumerSecret: "YOUR_MPESA_CONSUMER_SECRET",
  shortcode: "YOUR_MPESA_SHORTCODE",
  passkey: "YOUR_MPESA_PASSKEY",
  baseUrl: "https://sandbox.safaricom.co.ke",
};

// ======================================
// 1. Create Stripe Subscription
// ======================================
app.post("/create-subscription", async (req, res) => {
  try {
    const { priceId, customerEmail } = req.body;

    // Create customer
    const customer = await stripe.customers.create({
      email: customerEmail,
    });

    // Create subscription
    const subscription = await stripe.subscriptions.create({
      customer: customer.id,
      items: [{ price: priceId }],
      payment_behavior: "default_incomplete",
      expand: ["latest_invoice.payment_intent"],
    });

    res.json({ subscriptionId: subscription.id, clientSecret: subscription.latest_invoice.payment_intent.client_secret });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// ======================================
// 2. M-Pesa Wallet Top-up (STK Push)
// ======================================
app.post("/wallet-topup", async (req, res) => {
  try {
    const { phone, amount } = req.body;

    // 1. Get OAuth Token
    const auth = Buffer.from(`${mpesaConfig.consumerKey}:${mpesaConfig.consumerSecret}`).toString("base64");
    const tokenResponse = await axios.get(`${mpesaConfig.baseUrl}/oauth/v1/generate?grant_type=client_credentials`, {
      headers: { Authorization: `Basic ${auth}` },
    });

    const accessToken = tokenResponse.data.access_token;

    // 2. Trigger STK Push
    const timestamp = new Date().toISOString().replace(/[-T:.Z]/g, "").slice(0, 14);
    const password = Buffer.from(`${mpesaConfig.shortcode}${mpesaConfig.passkey}${timestamp}`).toString("base64");

    const stkResponse = await axios.post(
      `${mpesaConfig.baseUrl}/mpesa/stkpush/v1/processrequest`,
      {
        BusinessShortCode: mpesaConfig.shortcode,
        Password: password,
        Timestamp: timestamp,
        TransactionType: "CustomerPayBillOnline",
        Amount: amount,
        PartyA: phone, // User's phone
        PartyB: mpesaConfig.shortcode,
        PhoneNumber: phone,
        CallBackURL: "https://yourdomain.com/mpesa/callback",
        AccountReference: "StudyBuddyWallet",
        TransactionDesc: "Wallet Top-up",
      },
      { headers: { Authorization: `Bearer ${accessToken}` } }
    );

    res.json({ message: "STK push sent", data: stkResponse.data });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

// ======================================
// 3. M-Pesa Callback (updates wallet balance)
// ======================================
app.post("/mpesa/callback", (req, res) => {
  const { Body } = req.body;

  if (Body.stkCallback.ResultCode === 0) {
    // ✅ Payment Successful → Update Wallet Balance in DB
    const amount = Body.stkCallback.CallbackMetadata.Item.find(i => i.Name === "Amount").Value;
    const phone = Body.stkCallback.CallbackMetadata.Item.find(i => i.Name === "PhoneNumber").Value;

    console.log(`Wallet top-up successful: ${phone} +${amount}`);
    // Update user wallet balance in database here
  }

  res.json({ status: "ok" });
});

// ======================================
// Start Server
// ======================================
app.listen(5000, () => console.log("Server running on http://localhost:5000"));
