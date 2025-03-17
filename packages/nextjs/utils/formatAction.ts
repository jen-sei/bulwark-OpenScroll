const formatAction = (action: string) => {
  if (!action) return "";

  const formatted = action.replace(/_/g, " ");

  const lowercased = formatted
    .replace(/([A-Z])/g, " $1")
    .trim()
    .toLowerCase();

  return lowercased.charAt(0).toUpperCase() + lowercased.slice(1);
};

export default formatAction;
