const BASE_URL = 'http://localhost:8000/api';

export const getVessels = async () => {
  try {
    const response = await fetch(`${BASE_URL}/vessels`);

    if (!response.ok) {
      throw new Error('Failed to fetch vessels');
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching vessels:', error);
    throw error;
  }
};
