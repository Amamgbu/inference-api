import axios from "axios";

export async function queryCountryAPI(lang, title, threshold) {
  // TODO: API URL from configuration.
  const response = await axios.get(
    `/api/v1/get-summary?lang=${lang}&title=${title}&threshold=${threshold}`
  );
  return response.data;
}
