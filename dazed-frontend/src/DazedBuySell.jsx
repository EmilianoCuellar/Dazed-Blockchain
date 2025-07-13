import { useState, useEffect } from 'react';
import axios from 'axios';

export default function DazedBuySell() {
  const [wallet, setWallet] = useState('');
  const [usdToBuy, setUsdToBuy] = useState('');
  const [dazedToSell, setDazedToSell] = useState('');
  const [balance, setBalance] = useState(null);
  const [price, setPrice] = useState(null);
  const [marketCap, setMarketCap] = useState(null);
  const [status, setStatus] = useState('');

  const API_BASE = 'http://localhost:5000';

  const fetchInfo = async () => {
    const [priceRes, capRes] = await Promise.all([
      axios.get(`${API_BASE}/token/price`),
      axios.get(`${API_BASE}/token/marketcap`)
    ]);
    setPrice(priceRes.data.current_price);
    setMarketCap(capRes.data.market_cap);
  };

  const fetchBalance = async () => {
    if (!wallet) return;
    const res = await axios.get(`${API_BASE}/token/balance/${wallet}`);
    setBalance(res.data.balance);
  };

  const buyDazed = async () => {
    try {
      const res = await axios.post(`${API_BASE}/token/buy`, { wallet, usd: usdToBuy });
      setStatus(res.data.message);
      fetchBalance();
      fetchInfo();
    } catch (err) {
      setStatus('Buy failed.');
    }
  };

  const sellDazed = async () => {
    try {
      const res = await axios.post(`${API_BASE}/token/sell`, { wallet, amount: dazedToSell });
      setStatus(res.data.message);
      fetchBalance();
      fetchInfo();
    } catch (err) {
      setStatus('Sell failed.');
    }
  };

  useEffect(() => {
    fetchInfo();
    if (wallet) fetchBalance();
  }, [wallet]);

  return (
    <div className="min-h-screen bg-gray-950 text-white px-6 py-12 flex flex-col items-center">
      <h1 className="text-4xl font-bold mb-6">$Dazed Exchange</h1>

      <input
        type="text"
        value={wallet}
        onChange={(e) => setWallet(e.target.value)}
        placeholder="Enter your wallet address"
        className="mb-4 px-4 py-2 rounded bg-gray-800 border border-gray-700 w-full max-w-md"
      />

      {balance !== null && (
        <p className="mb-4">Balance: <span className="font-bold">{balance} $Dazed</span></p>
      )}

      {price !== null && marketCap !== null && (
        <div className="mb-6 text-sm text-gray-300">
          <p>Current Price: ${price} / $Dazed</p>
          <p>Market Cap: ${marketCap}</p>
        </div>
      )}

      <div className="flex flex-col sm:flex-row gap-6">
        <div>
          <h2 className="text-xl font-semibold mb-2">Buy $Dazed</h2>
          <input
            type="number"
            value={usdToBuy}
            onChange={(e) => setUsdToBuy(e.target.value)}
            placeholder="USD amount"
            className="mb-2 px-4 py-2 rounded bg-gray-800 border border-gray-700 w-full"
          />
          <button
            onClick={buyDazed}
            className="w-full bg-green-500 hover:bg-green-600 text-black font-semibold px-4 py-2 rounded"
          >
            Buy
          </button>
        </div>

        <div>
          <h2 className="text-xl font-semibold mb-2">Sell $Dazed</h2>
          <input
            type="number"
            value={dazedToSell}
            onChange={(e) => setDazedToSell(e.target.value)}
            placeholder="$Dazed amount"
            className="mb-2 px-4 py-2 rounded bg-gray-800 border border-gray-700 w-full"
          />
          <button
            onClick={sellDazed}
            className="w-full bg-red-500 hover:bg-red-600 text-white font-semibold px-4 py-2 rounded"
          >
            Sell
          </button>
        </div>
      </div>

      {status && <p className="mt-6 text-sm text-yellow-400">{status}</p>}
    </div>
  );
}
