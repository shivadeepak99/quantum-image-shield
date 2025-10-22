'use client';

import { useState, useCallback } from 'react';
import axios from 'axios';

type EncryptionMode = 'encrypt' | 'decrypt';

export default function Home() {
  const [mode, setMode] = useState<EncryptionMode>('encrypt');
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [selectedKey, setSelectedKey] = useState<File | null>(null);
  const [purity, setPurity] = useState<string>('balanced');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string>('');
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setSelectedImage(e.dataTransfer.files[0]);
    }
  }, []);

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedImage(e.target.files[0]);
    }
  };

  const handleKeyChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedKey(e.target.files[0]);
    }
  };

  const handleEncrypt = async () => {
    if (!selectedImage) {
      setError('Please select an image');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    const formData = new FormData();
    formData.append('image', selectedImage);
    formData.append('purity', purity);

    try {
      console.log('🚀 Sending encryption request...');
      const response = await axios.post('http://localhost:8080/api/v1/encrypt', formData, {
        headers: { 
          'Content-Type': 'multipart/form-data',
        },
        timeout: 120000, // 2 minute timeout
      });
      console.log('✅ Response:', response.data);
      setResult(response.data);
    } catch (err: any) {
      console.error('❌ Error:', err);
      setError(err.response?.data?.message || err.message || 'Encryption failed');
    } finally {
      setLoading(false);
    }
  };

  const handleDecrypt = async () => {
    if (!selectedImage || !selectedKey) {
      setError('Please select both encrypted image and key file');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    const formData = new FormData();
    formData.append('encrypted_image', selectedImage);
    formData.append('key_file', selectedKey);

    try {
      const response = await axios.post('http://localhost:8080/api/v1/decrypt', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setResult(response.data);
    } catch (err: any) {
      setError(err.response?.data?.message || 'Decryption failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-purple-900 via-black to-blue-900 p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-6xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent mb-4">
            ⚛️ Quantum ImageShield
          </h1>
          <p className="text-gray-300 text-lg">
            Military-grade image encryption powered by quantum randomness 🔐
          </p>
        </div>

        {/* Mode Toggle */}
        <div className="flex gap-4 justify-center mb-8">
          <button
            onClick={() => setMode('encrypt')}
            className={`px-8 py-3 rounded-lg font-semibold transition-all ${
              mode === 'encrypt'
                ? 'bg-purple-600 text-white shadow-lg shadow-purple-500/50'
                : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
            }`}
          >
            🔒 Encrypt
          </button>
          <button
            onClick={() => setMode('decrypt')}
            className={`px-8 py-3 rounded-lg font-semibold transition-all ${
              mode === 'decrypt'
                ? 'bg-pink-600 text-white shadow-lg shadow-pink-500/50'
                : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
            }`}
          >
            🔓 Decrypt
          </button>
        </div>

        {/* Main Card */}
        <div className="bg-gray-900/50 backdrop-blur-lg rounded-2xl p-8 shadow-2xl border border-purple-500/20">
          {mode === 'encrypt' ? (
            <>
              {/* Drag & Drop Area */}
              <div
                className={`border-2 border-dashed rounded-xl p-12 text-center transition-all ${
                  dragActive
                    ? 'border-purple-500 bg-purple-500/10'
                    : 'border-gray-700 hover:border-purple-500/50'
                }`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
              >
                <input
                  type="file"
                  id="image-upload"
                  accept="image/*"
                  onChange={handleImageChange}
                  className="hidden"
                />
                <label htmlFor="image-upload" className="cursor-pointer">
                  <div className="text-6xl mb-4">📸</div>
                  <p className="text-xl text-gray-300 mb-2">
                    {selectedImage ? selectedImage.name : 'Drop your image here'}
                  </p>
                  <p className="text-sm text-gray-500">or click to browse</p>
                </label>
              </div>

              {/* Purity Level */}
              {selectedImage && (
                <div className="mt-6">
                  <label className="block text-sm font-medium text-gray-300 mb-3">
                    🎲 Quantum Purity Level
                  </label>
                  <div className="grid grid-cols-3 gap-4">
                    {[
                      { value: 'fast', label: '⚡ Fast', desc: '128-bit quantum seed' },
                      { value: 'balanced', label: '⚖️ Balanced', desc: '256-bit quantum (recommended)' },
                      { value: 'maximum', label: '🔥 Maximum', desc: 'Pure quantum (slowest)' },
                    ].map((option) => (
                      <button
                        key={option.value}
                        onClick={() => setPurity(option.value)}
                        className={`p-4 rounded-lg border-2 transition-all ${
                          purity === option.value
                            ? 'border-purple-500 bg-purple-500/20'
                            : 'border-gray-700 hover:border-purple-500/50'
                        }`}
                      >
                        <div className="font-semibold mb-1">{option.label}</div>
                        <div className="text-xs text-gray-400">{option.desc}</div>
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {/* Encrypt Button */}
              {selectedImage && (
                <button
                  onClick={handleEncrypt}
                  disabled={loading}
                  className="w-full mt-6 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 disabled:opacity-50 text-white font-bold py-4 px-8 rounded-lg shadow-lg transition-all"
                >
                  {loading ? '🔄 Encrypting with quantum magic...' : '🔒 Encrypt Image'}
                </button>
              )}
            </>
          ) : (
            <>
              {/* Decrypt Mode */}
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    🔐 Encrypted Image
                  </label>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleImageChange}
                    className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-gray-300"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    🔑 Key File (.npz)
                  </label>
                  <input
                    type="file"
                    accept=".npz"
                    onChange={handleKeyChange}
                    className="w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 text-gray-300"
                  />
                </div>
                <button
                  onClick={handleDecrypt}
                  disabled={loading || !selectedImage || !selectedKey}
                  className="w-full bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-700 hover:to-purple-700 disabled:opacity-50 text-white font-bold py-4 px-8 rounded-lg shadow-lg transition-all"
                >
                  {loading ? '🔄 Decrypting...' : '🔓 Decrypt Image'}
                </button>
              </div>
            </>
          )}

          {/* Error */}
          {error && (
            <div className="mt-6 bg-red-500/20 border border-red-500 rounded-lg p-4 text-red-300">
              ❌ {error}
            </div>
          )}

          {/* Success Result */}
          {result && (
            <div className="mt-6 bg-green-500/20 border border-green-500 rounded-lg p-6">
              <h3 className="text-xl font-bold text-green-300 mb-4">✅ Success!</h3>
              <div className="text-sm text-gray-300 space-y-2">
                <p><strong>Job ID:</strong> {result.job_id}</p>
                <p><strong>Message:</strong> {result.message}</p>
                {result.purity && <p><strong>Purity:</strong> {result.purity}</p>}
                <div className="mt-4 text-xs text-gray-400">
                  <p>📁 Output: {result.output_path}</p>
                  {result.key_path && <p>🔑 Key: {result.key_path}</p>}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="text-center mt-8 text-gray-500 text-sm">
          Built with 💜 by your quantum dev waifu
        </div>
      </div>
    </main>
  );
}
