import { atom } from "jotai";
import { Entity, ApiState } from "@/store/types";
import { atomWithMutation, atomWithQuery } from "jotai-tanstack-query";
import { fetchGet, fetchPost, fetchPut, fetchDelete } from "@/utils/apiUtils";

export function createApiStore<T extends Entity>(apiEndpoint: string) {
  const baseState: ApiState<T> = {
    data: [],
    loading: false,
    error: null,
  };

  const stateAtom = atom<ApiState<T>>(baseState);

  const selectedIdAtom = atom<string | number | null>(null);

  const fetchAllAtom = atomWithQuery(() => ({
    queryKey: ["items", apiEndpoint],
    queryFn: () => fetchGet(apiEndpoint),
  }));

  const fetchOneAtom = atomWithQuery((get) => {
    const id = get(selectedIdAtom);
    return {
      queryKey: ["item", apiEndpoint, id],
      queryFn: async () => {
        if (id === null) {
          throw new Error("No ID selected");
        }
        return await fetchGet(`${apiEndpoint}/${id}`);
      },
      enabled: Boolean(id),
    };
  });

  const createAtom = atomWithMutation(() => ({
    mutationKey: ["create", apiEndpoint],
    mutationFn: (data: Omit<T, "id">) => fetchPost(apiEndpoint, data),
  }));

  const updateAtom = atomWithMutation(() => ({
    mutationKey: ["update", apiEndpoint],
    mutationFn: ({ id, data }: { id: string | number; data: Partial<T> }) =>
      fetchPut(`${apiEndpoint}/${id}`, data),
  }));

  const deleteAtom = atomWithMutation(() => ({
    mutationKey: ["delete", apiEndpoint],
    mutationFn: (id: string | number) => fetchDelete(`${apiEndpoint}/${id}`),
  }));

  return {
    stateAtom,
    fetchAllAtom,
    fetchOneAtom,
    createAtom,
    updateAtom,
    deleteAtom,
    selectedIdAtom,
  };
}
