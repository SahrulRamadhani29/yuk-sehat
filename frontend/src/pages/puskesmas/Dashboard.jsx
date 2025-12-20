import React, { useEffect, useState } from "react";
import Container from "../../components/layout/Container";
import Badge from "../../components/ui/Badge";

const Dashboard = () => {
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);

  const API_BASE = import.meta.env.VITE_API_BASE_URL;

  useEffect(() => {
    fetch(`${API_BASE}/triage-logs`)
      .then((res) => res.json())
      .then((data) => {
        const redCases = data.filter(
          (item) => item.triage_result === "MERAH"
        );
        setPatients(redCases);
      })
      .catch((err) => {
        console.error("Gagal mengambil data dashboard:", err);
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <Container className="bg-[#f6f3f2] min-h-screen p-8 max-w-none">
      {/* MOBILE WARNING */}
      <div className="block lg:hidden text-center mt-20 text-gray-500">
        <p className="text-lg font-semibold">
          Dashboard Puskesmas
        </p>
        <p className="mt-2 text-sm">
          Dashboard ini dirancang untuk tampilan desktop (PC).
        </p>
      </div>

      {/* DESKTOP CONTENT */}
      <div className="hidden lg:block max-w-[1600px] mx-auto">
        {/* HEADER */}
        <div className="mb-8 flex justify-between items-end">
          <div>
            <h1 className="text-3xl font-bold text-gray-800">
              Dashboard Puskesmas
            </h1>
            <p className="text-sm text-gray-500 mt-1">
              Daftar Pasien Darurat (MERAH)
            </p>
          </div>
        </div>

        {loading && <p>Memuat data...</p>}

        {/* GRID PASIEN */}
        <div className="grid grid-cols-3 2xl:grid-cols-4 gap-8">
          {patients.map((p) => (
            <div
              key={p.id}
              className="bg-red-50 border border-red-400 rounded-2xl p-6 shadow-sm"
            >
              {/* HEADER KARTU */}
              <div className="flex justify-between items-center mb-4">
                <Badge variant="danger">MERAH</Badge>
                <span className="text-xs text-gray-500">
                  #{p.id}
                </span>
              </div>

              {/* IDENTITAS */}
              <div className="space-y-1 text-sm">
                <p className="font-semibold text-gray-800">
                  NIK: {p.nik}
                </p>
                <p className="text-gray-600">
                  Umur: {p.age} tahun
                </p>
              </div>

              {/* KELUHAN */}
              <div className="mt-3 text-sm text-gray-700 line-clamp-2">
                {p.complaint}
              </div>

              {/* FOOTER */}
              <div className="mt-5 flex justify-between items-center text-xs text-gray-500">
                <span className="uppercase font-semibold text-red-600">
                  {p.category}
                </span>
                <span>
                  {new Date(p.created_at).toLocaleTimeString("id-ID", {
                    hour: "2-digit",
                    minute: "2-digit",
                  })} WIB
                </span>
              </div>
            </div>
          ))}
        </div>

        {!loading && patients.length === 0 && (
          <p className="text-gray-500 mt-12">
            Tidak ada pasien darurat hari ini.
          </p>
        )}
      </div>
    </Container>
  );
};

export default Dashboard;
