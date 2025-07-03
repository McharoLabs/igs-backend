import { describe, it, expect } from "vitest";
import Button from "../common/Button";
import { render, screen } from "@testing-library/react";

describe("Button component", () => {
  it("renders correctly", () => {
    render(<Button type="button">Click me</Button>);
    expect(screen.getByText("Click me")).toBeDefined();
  });
});
