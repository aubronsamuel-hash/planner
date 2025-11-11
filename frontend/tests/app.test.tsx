import { beforeEach, describe, expect, it } from "vitest";

describe("App bootstrap", () => {
  beforeEach(() => {
    document.body.innerHTML = "<div id='root'></div>";
  });

  it("renders without crashing", async () => {
    await import("../src/main");
    expect(document.getElementById("root")).toBeTruthy();
  });
});
