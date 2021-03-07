import axios from "axios";

export async function getRandomTitle(lang) {
  const response = await axios.get(
    `https://${lang}.wikipedia.org/w/api.php?action=query&format=json&list=random&rnlimit=1&rnnamespace=0&origin=*`
  );

  return response.data.query.random[0].title;
}
