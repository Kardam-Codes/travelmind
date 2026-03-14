import { useEffect, useMemo } from "react";
import { getActiveOrgId, getStoredUser, setActiveOrgId } from "../utils/session";

function OrgSwitcher() {
  const storedUser = getStoredUser();
  const organizations = storedUser?.organizations || [];
  const activeOrgId = getActiveOrgId() || storedUser?.default_org_id;

  const sortedOrgs = useMemo(() => {
    return [...organizations].sort((a, b) => a.name.localeCompare(b.name));
  }, [organizations]);

  useEffect(() => {
    if (!getActiveOrgId() && storedUser?.default_org_id) {
      setActiveOrgId(storedUser.default_org_id);
    }
  }, [storedUser]);

  if (!sortedOrgs.length) {
    return null;
  }

  return (
    <select
      className="h-11 rounded-full bg-white/70 px-4 text-sm font-medium text-text shadow-float transition-colors dark:bg-white/10 dark:text-white"
      onChange={(event) => setActiveOrgId(event.target.value)}
      value={activeOrgId || ""}
    >
      {sortedOrgs.map((org) => (
        <option key={org.id} value={org.id}>
          {org.name}
        </option>
      ))}
    </select>
  );
}

export default OrgSwitcher;
