import { useState } from "react";
import axios from "axios";

const Pendaftaran = () => {
  const [response, setResponse] = useState(null);
  const [formData, setFormData] = useState({
    ipk: "",
    jarak: "",
    jenisKelamin: "",
    organisasi: "",
    penghasilan: "",
    sks: "",
    ukm: "",
    tanggungan: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Pastikan nilai yang dikirim sesuai dengan format backend
    const dataToSend = {
      IPK: formData.ipk,
      Penghasilan: formData.penghasilan, // Pastikan sesuai dengan mapping di backend
      Tanggungan: formData.tanggungan,
      Jarak: formData.jarak, // Pastikan sesuai dengan mapping di backend
      Organisasi: formData.organisasi, // "Ikut" atau "Tidak"
      UKM: formData.ukm, // "Ikut" atau "Tidak"
      JenisKelamin: formData.jenisKelamin === "Laki-laki" ? "L" : "P", // Sesuai mapping backend
      SKS: formData.sks,
    };

    try {
      const response = await axios.post(
        "http://localhost:5000/predict",
        dataToSend,
        {
          headers: { "Content-Type": "application/json" },
        }
      );
      console.log("Response:", response.data);
      setResponse(response.data);
    } catch (error) {
      setResponse(error.response ? error.response.data : error.message);
      console.error(
        "Error:",
        error.response ? error.response.data : error.message
      );
    }
  };

  return (
    <div>
      <div>
        <h1>Beasiswa Mahasiswa Pintar</h1>
        <p className="text-start">Syarat daftar Beasiswa</p>
        <div className="bg-slate-300 w-full h-44"></div>
        <p>Form Pendaftaran Beasiswa</p>
        <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-gray-700">IPK</label>
            <input
              type="number"
              name="ipk"
              value={formData.ipk}
              onChange={handleChange}
              step="0.01"
              className="w-full p-2 border rounded"
              required
            />
          </div>

          <div>
            <label className="block text-gray-700">Jarak</label>
            <select
              name="jarak"
              value={formData.jarak}
              onChange={handleChange}
              className="w-full p-2 border rounded"
              required
            >
              <option value="">Pilih</option>
              <option value="Dekat">Dekat</option>
              <option value="Jauh">Jauh</option>
            </select>
          </div>

          <div>
            <label className="block text-gray-700">Jenis Kelamin</label>
            <select
              name="jenisKelamin"
              value={formData.jenisKelamin}
              onChange={handleChange}
              className="w-full p-2 border rounded"
              required
            >
              <option value="">Pilih</option>
              <option value="Laki-laki">Laki-laki</option>
              <option value="Perempuan">Perempuan</option>
            </select>
          </div>

          <div>
            <label className="block text-gray-700">Organisasi</label>
            <select
              name="organisasi"
              value={formData.organisasi}
              onChange={handleChange}
              className="w-full p-2 border rounded"
              required
            >
              <option value="">Pilih</option>
              <option value="Ikut">Ikut</option>
              <option value="Tidak">Tidak</option>
            </select>
          </div>

          <div>
            <label className="block text-gray-700">
              Penghasilan Orang Tua (Rp)
            </label>
            <select
              name="penghasilan"
              value={formData.penghasilan}
              onChange={handleChange}
              className="w-full p-2 border rounded"
              required
            >
              <option value="">Pilih</option>
              <option value="Rendah">Rendah</option>
              <option value="Sedang">Sedang</option>
              <option value="Tinggi">Tinggi</option>
            </select>
          </div>

          <div>
            <label className="block text-gray-700">SKS</label>
            <input
              type="number"
              name="sks"
              value={formData.sks}
              onChange={handleChange}
              className="w-full p-2 border rounded"
              required
            />
          </div>

          <div>
            <label className="block text-gray-700">UKM</label>
            <select
              name="ukm"
              value={formData.ukm}
              onChange={handleChange}
              className="w-full p-2 border rounded"
              required
            >
              <option value="">Pilih</option>
              <option value="Ikut">Ikut</option>
              <option value="Tidak">Tidak</option>
            </select>
          </div>

          <div>
            <label className="block text-gray-700">Jumlah Tanggungan</label>
            <input
              type="number"
              name="tanggungan"
              value={formData.tanggungan}
              onChange={handleChange}
              className="w-full p-2 border rounded"
              required
            />
          </div>

          <div className="col-span-2">
            <button
              type="submit"
              className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600"
            >
              Submit
            </button>
          </div>
        </form>
        {response && (
  <div
    className={`mt-4 p-2 text-white rounded ${
      response.prediction_code === 1
        ? "bg-green-500"
        : "bg-red-500"
    }`}
  >
    <div>
      <p>Presentase Kemungkinan:</p>
      <ul>
        <li>
          Tidak Menerima Beasiswa: {(response.probability["Tidak Menerima Beasiswa"] * 100).toFixed(2)}%
        </li>
        <li>
          Menerima Beasiswa: {(response.probability["Menerima Beasiswa"] * 100).toFixed(2)}%
        </li>
      </ul>
    </div>
    <p>Hasil Prediksi: {response.prediction}</p>
  </div>
)}
      </div>
    </div>
  );
};

export default Pendaftaran;
