import { useEffect, useState } from 'react';

interface Device {
  ip: string;
  hostname?: string;
  mac?: string;
  open_ports: number[];
  status: string;
  device_type?: string;
  last_seen?: string;
  credentials?: {
    username?: string;
    password?: string;
    protocol?: string;
  };
}

export default function Home() {
  const [devices, setDevices] = useState<Device[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedDevice, setSelectedDevice] = useState<Device | null>(null);
  const [form, setForm] = useState({ device_type: '', protocol: '', username: '', password: '' });

  useEffect(() => {
    fetch("https://netorb.onrender.com/devices")
      .then((res) => res.json())
      .then((data) => {
        setDevices(data);
        setLoading(false);
      });
  }, []);

  const openModal = (device: Device) => {
    setSelectedDevice(device);
    setForm({
      device_type: device.device_type || '',
      protocol: device.credentials?.protocol || '',
      username: device.credentials?.username || '',
      password: device.credentials?.password || ''
    });
  };

  const closeModal = () => {
    setSelectedDevice(null);
  };

  const handleSubmit = async () => {
    if (!selectedDevice) return;
    const updated = { ...selectedDevice, device_type: form.device_type, credentials: { ...form } };
    await fetch(`"https://netorb.onrender.com/devices"/${selectedDevice.ip}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(updated)
    });
    closeModal();
    location.reload();
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Discovered Devices</h1>
      {loading ? (
        <p>Loading...</p>
      ) : devices.length === 0 ? (
        <p>No devices found.</p>
      ) : (
        <table className="min-w-full border border-gray-200">
          <thead>
            <tr className="bg-gray-100">
              <th className="p-2 border">IP</th>
              <th className="p-2 border">Hostname</th>
              <th className="p-2 border">MAC</th>
              <th className="p-2 border">Open Ports</th>
              <th className="p-2 border">Status</th>
              <th className="p-2 border">Device Type</th>
              <th className="p-2 border">Actions</th>
            </tr>
          </thead>
          <tbody>
            {devices.map((device) => (
              <tr key={device.ip} className="border-t">
                <td className="p-2 border">{device.ip}</td>
                <td className="p-2 border">{device.hostname || '-'}</td>
                <td className="p-2 border">{device.mac || '-'}</td>
                <td className="p-2 border">{device.open_ports.join(', ')}</td>
                <td className="p-2 border">{device.status}</td>
                <td className="p-2 border">{device.device_type || '-'}</td>
                <td className="p-2 border">
                  <button className="bg-blue-500 text-white px-2 py-1 rounded" onClick={() => openModal(device)}>
                    Edit
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {selectedDevice && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex justify-center items-center">
          <div className="bg-white p-6 rounded shadow-lg w-[400px]">
            <h2 className="text-xl font-bold mb-4">Edit Device: {selectedDevice.ip}</h2>

            <label className="block mb-2">Device Type</label>
            <select className="w-full mb-4 p-2 border rounded" value={form.device_type} onChange={(e) => setForm({ ...form, device_type: e.target.value })}>
              <option value="">Select</option>
              <option value="router">Router</option>
              <option value="switch">Switch</option>
              <option value="firewall">Firewall</option>
            </select>

            <label className="block mb-2">Protocol</label>
            <select className="w-full mb-4 p-2 border rounded" value={form.protocol} onChange={(e) => setForm({ ...form, protocol: e.target.value })}>
              <option value="">Select</option>
              <option value="ssh">SSH</option>
              <option value="snmp">SNMP</option>
            </select>

            <label className="block mb-2">Username</label>
            <input type="text" className="w-full mb-4 p-2 border rounded" value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })} />

            <label className="block mb-2">Password</label>
            <input type="password" className="w-full mb-4 p-2 border rounded" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} />

            <div className="flex justify-end gap-2">
              <button className="bg-gray-300 px-4 py-2 rounded" onClick={closeModal}>Cancel</button>
              <button className="bg-green-500 text-white px-4 py-2 rounded" onClick={handleSubmit}>Save</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
