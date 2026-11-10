
import axios from "axios";

const API_BASE_URL = "http://localhost:8000/api";

export const uploadPDD = async (file) => {
  const formData = new FormData();

  formData.append("file", file);

  const response = await axios.post(
    `${API_BASE_URL}/upload-pdd`,
    formData
  );

  return response.data;
};

export const generateSDD = async (projectName, pddText) => {
  const response = await axios.post(
    `${API_BASE_URL}/generate-sdd`,
    {
      project_name: projectName,
      pdd_text: pddText,
    }
  );

  return response.data;
};



export const exportSDD = async (sdd, format) => {
  const response = await axios.post(
    `${API_BASE_URL}/sdd/export/${format}`,
    {
      project_name: sdd.project_name,
      sdd: sdd,
    },
    {
      responseType: "blob",
    }
  );

  return response.data;
};

