import { useState } from 'react';
import axios from 'axios';
import DazedBuySell from "./DazedBuySell.jsx";
import BlockExplorer from './BlockExplorer';

function Dashboard() {
  const [wallet, setWallet] = useState('');
  const [commitment, setCommitment] = useState('');
  const [verified, setVerified] = useState(null);
  const [balance, setBalance] = useState(null);
  const [status, setStatus] = useState('');

  const API_BASE = 'http://localhost:5000'; // Your Flask backend

  const verifyZkId = async () => {
    try {
      setStatus('Verifying zk-ID...');
      const res = await axios.post(`${API_BASE}/zk-id/verify`, {
        commitment,
        wallet,
      });
      setVerified(res.data.verified);
      setStatus(res.data.message);
      fetchBalance();
    } catch (err) {
      setStatus(err.response?.data?.message || 'Verification failed');
      setVerified(false);
    }
  };

  const fetchBalance = async () => {
    try {
      const res = await axios.get(`${API_BASE}/token/balance/${wallet}`);
      setBalance(res.data.balance);
    } catch (err) {
      setBalance(null);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-800 text-white px-4 py-12 space-y-12">
      <div className="flex flex-col items-center justify-center">
        <h1 className="text-4xl font-bold mb-8 tracking-wide text-center">
          $Dazed zk-ID Verification
        </h1>

        <div className="w-full max-w-md space-y-4 bg-gray-900 p-6 rounded-2xl shadow-lg border border-gray-700">
          {/* zk-ID Wallet Input */}
          <input
            type="text"
            value={wallet}
            onChange={(e) => setWallet(e.target.value)}
            placeholder="Enter your wallet address"
            className="w-full px-4 py-2 rounded-lg bg-gray-800 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-green-500"
          />

          {/* zk-ID Commitment Input */}
          <input
            type="text"
            value={commitment}
            onChange={(e) => setCommitment(e.target.value)}
            placeholder="Paste your zk-ID commitment hash"
            className="w-full px-4 py-2 rounded-lg bg-gray-800 border border-gray-700 focus:outline-none focus:ring-2 focus:ring-green-500"
          />

          {/* zk-ID Verification Button */}
          <button
            onClick={verifyZkId}
            className="w-full px-6 py-2 rounded-xl bg-green-500 hover:bg-green-600 text-black font-semibold transition duration-200"
          >
            Verify zk-ID
          </button>

          {/* Status and Result */}
          {status && (
            <div className="text-sm text-gray-300 text-center pt-2">{status}</div>
          )}
          {balance !== null && (
            <div className="text-center text-lg pt-1">
              Wallet Balance: <span className="font-bold">{balance} $Dazed</span>
            </div>
          )}
          {verified !== null && (
            <div className={`text-center pt-1 font-semibold ${verified ? 'text-green-400' : 'text-red-400'}`}>
              {verified ? '✅ Verified' : '❌ Not Verified'}
            </div>
          )}
        </div>
      </div>

      {/* 💸 Buy & Sell Interface */}
      <div className="w-full max-w-4xl mx-auto">
        <DazedBuySell />
      </div>

      {/* 🔎 Block Explorer */}
      <div className="w-full max-w-6xl mx-auto">
        <BlockExplorer />
      </div>
    </div>
  );
}

export default Dashboard;
