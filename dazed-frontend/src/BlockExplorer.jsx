import { useEffect, useState } from "react";
import axios from "axios";

export default function BlockExplorer() {
  const [chain, setChain] = useState([]);

  useEffect(() => {
    const fetchChain = async () => {
      console.log("📡 Fetching blockchain...");
      try {
        const res = await fetch("http://localhost:5002/chain");
  
        if (!res.ok) {
          throw new Error("Network response was not ok");
        }
  
        const data = await res.json();
        console.log("Blockchain data:", data);
        setChain(data.chain.reverse());
      } catch (err) {
        console.error("Error fetching blockchain:", err);
      }
    };
  
    fetchChain();
  }, []);
  

  return (
    <div className="min-h-screen bg-gray-950 text-white px-6 py-12">
      <h1 className="text-3xl font-bold text-center mb-8">$Dazed Block Explorer</h1>
      <div className="space-y-6">
        {chain.map((block) => (
          <div key={block.hash} className="bg-gray-900 p-6 rounded-xl border border-gray-700">
            <h2 className="text-xl font-bold">Block #{block.index ?? 'N/A'}</h2>
            <p className="text-sm text-gray-400">⛓️ Hash: {block.hash}</p>
            <p className="text-sm text-gray-500">🧱 Prev: {block.previous_hash}</p>
            <p className="text-sm text-gray-500">🕓 {block.timestamp ? new Date(block.timestamp * 1000).toLocaleString() : 'Unknown'}</p>
            <div className="mt-4">
              <p className="font-semibold text-green-400">Transactions:</p>
              <ul className="list-disc list-inside mt-1 space-y-1">
                {block.transactions.map((tx, idx) => (
                  <li key={idx} className="text-sm">
                    {tx.type === "mint" && (
                      <span>Minted <b>{tx.amount}</b> $Dazed → {tx.to}</span>
                    )}
                    {tx.type === "transfer" && (
                      <span>{tx.from} → <b>{tx.amount}</b> $Dazed → {tx.to}</span>
                    )}
                    {tx.note && <span className="block text-gray-400 italic">Note: {tx.note}</span>}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
