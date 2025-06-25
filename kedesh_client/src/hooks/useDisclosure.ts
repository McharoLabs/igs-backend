import { useState } from "react";

type UseDisclosureHandlers = {
  open: () => void;
  close: () => void;
  toggle: () => void;
};

type UseDisclosureReturn = [boolean, UseDisclosureHandlers];

function useDisclosure(initialState: boolean = false): UseDisclosureReturn {
  const [opened, setOpened] = useState<boolean>(initialState);

  const handlers: UseDisclosureHandlers = {
    open: () => setOpened(true),
    close: () => setOpened(false),
    toggle: () => setOpened((prev) => !prev),
  };

  return [opened, handlers];
}

export default useDisclosure;
