import { useState, useEffect } from 'react';
import axios from 'axios';
import PoPVerificationForm from "./PoPVerificationForm";

export default function DazedDashboard() {
  const [commitment, setCommitment] = useState('');
  const [verified, setVerified] = useState(null);
  const [balance, setBalance] = useState(null);
  const [usdValue, setUsdValue] = useState(null);
  const [status, setStatus] = useState('');

  const API_BASE = 'http://localhost:5000';
  const FIXED_PRICE = 0.05; // $0.05 per Dazed

  const verifyZkId = async () => {
    try {
        setStatus('Verifying zk-ID...');
        const res = await axios.post(`${API_BASE}/zk-id/verify`, {
            commitment: commitment.trim(),
            wallet: wallet.trim(),
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
      setUsdValue((res.data.balance * FIXED_PRICE).toFixed(2));
    } catch (err) {
      setBalance(null);
      setUsdValue(null);
    }
  };

  return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center justify-center px-4 py-12">
      <h1 className="text-4xl font-bold mb-6">$Dazed zk-ID Verification</h1>
      <PoPVerificationForm />
      <input
        type="text"
        readOnly
        className="w-full max-w-md px-4 py-2 rounded-lg bg-gray-800 border border-gray-700 mb-4"
      />

      <input
        type="text"
        value={commitment}
        onChange={(e) => setCommitment(e.target.value)}
        placeholder="Paste your zk-ID commitment hash"
        className="w-full max-w-md px-4 py-2 rounded-lg bg-gray-800 border border-gray-700 mb-4"
      />

      <button
        onClick={verifyZkId}
        className="px-6 py-2 rounded-xl bg-green-500 hover:bg-green-600 text-black font-semibold"
      >
        Verify zk-ID
      </button>

      {status && <p className="mt-4 text-sm text-gray-300">{status}</p>}

      {balance !== null && (
        <p className="mt-2 text-lg">
          Wallet Balance: <span className="font-bold">{balance} $Dazed</span>
        </p>
      )}

      {usdValue !== null && (
        <p className="text-sm text-gray-400">
          Estimated Value: ${usdValue} USD
        </p>
      )}

      {verified !== null && (
        <p className={`mt-2 font-semibold ${verified ? 'text-green-400' : 'text-red-400'}`}>
          {verified ? '✅ Verified' : '❌ Not Verified'}
        </p>
      )}
    </div>
  );
}
