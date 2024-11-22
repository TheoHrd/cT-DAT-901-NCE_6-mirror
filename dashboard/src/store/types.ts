export interface Entity {
  id: string | number;
  [key: string]: unknown;
}

export interface ApiState<T extends Entity> {
  data: T[];
  loading: boolean;
  error: string | null;
}

