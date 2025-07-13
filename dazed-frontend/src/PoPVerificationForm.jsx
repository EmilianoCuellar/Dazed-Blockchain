import { useState } from "react";
import axios from "axios";

export default function PoPVerificationForm() {
  const [wallet, setWallet] = useState("");
  const [metrcId, setMetrcId] = useState("");
  const [commitment, setCommitment] = useState("");
  const [status, setStatus] = useState(null);

  const submitVerification = async () => {
    setStatus("Verifying product...");
    try {
      const res = await axios.post("http://localhost:5003/pop-verify", {
        wallet,
        metrc_id: metrcId,
        commitment,
      });
      setStatus(`✅ ${res.data.message} | Block #: ${res.data.block.index}`);
    } catch (err) {
      const msg = err.response?.data?.message || err.response?.data?.error || "Verification failed.";
      setStatus(`❌ ${msg}`);
    }
  };

  return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center justify-center p-6">
      <h1 className="text-3xl font-bold mb-4">Proof of Product Verification</h1>
      <div className="w-full max-w-md space-y-4">
        <input
          type="text"
          value={wallet}
          onChange={(e) => setWallet(e.target.value)}
          placeholder="Wallet address"
          className="w-full px-4 py-2 rounded bg-gray-800 border border-gray-700"
        />

        <input
          type="text"
          value={metrcId}
          onChange={(e) => setMetrcId(e.target.value)}
          placeholder="24-digit METRC ID"
          className="w-full px-4 py-2 rounded bg-gray-800 border border-gray-700"
        />

        <input
          type="text"
          value={commitment}
          onChange={(e) => setCommitment(e.target.value)}
          placeholder="zk-ID commitment hash"
          className="w-full px-4 py-2 rounded bg-gray-800 border border-gray-700"
        />

        <button
          onClick={submitVerification}
          className="w-full py-2 rounded bg-green-500 hover:bg-green-600 text-black font-semibold"
        >
          Submit Verification
        </button>

        {status && <p className="mt-2 text-sm text-center text-gray-300">{status}</p>}
      </div>
    </div>
  );
}
