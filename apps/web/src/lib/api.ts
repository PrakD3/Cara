import axios from "axios";

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
});

export const getPatientProfile = async () => {
  const { data } = await api.get("/api/patients/me");
  return data;
};

export const getMedications = async (patientId: string) => {
  const { data } = await api.get(`/api/medications/patient/${patientId}`);
  return data;
};

export default api;
