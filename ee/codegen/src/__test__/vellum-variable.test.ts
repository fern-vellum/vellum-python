import { Writer } from "@fern-api/python-ast/core/Writer";

import * as codegen from "src/codegen";

describe("VellumVariableField", () => {
  let writer: Writer;

  beforeEach(() => {
    writer = new Writer();
  });

  test("StringVellumVariable snapshot", async () => {
    const stringVar = codegen.vellumVariable({
      variable: { id: "1", name: "test", type: "STRING" },
    });
    stringVar.write(writer);
    expect(await writer.toStringFormatted()).toMatchSnapshot();
  });

  test("NumberVellumVariable snapshot", async () => {
    const numberVar = codegen.vellumVariable({
      variable: { id: "1", name: "test", type: "NUMBER" },
    });
    numberVar.write(writer);
    expect(await writer.toStringFormatted()).toMatchSnapshot();
  });

  test("JsonVellumVariable snapshot", async () => {
    const jsonVar = codegen.vellumVariable({
      variable: { id: "1", name: "test", type: "JSON" },
    });
    jsonVar.write(writer);
    expect(await writer.toStringFormatted()).toMatchSnapshot();
  });

  test("ImageVellumVariable snapshot", async () => {
    const imageVar = codegen.vellumVariable({
      variable: { id: "1", name: "test", type: "IMAGE" },
    });
    imageVar.write(writer);
    expect(await writer.toStringFormatted()).toMatchSnapshot();
  });

  test("FunctionCallVellumVariable snapshot", async () => {
    const functionCallVar = codegen.vellumVariable({
      variable: { id: "1", name: "test", type: "FUNCTION_CALL" },
    });
    functionCallVar.write(writer);
    expect(await writer.toStringFormatted()).toMatchSnapshot();
  });

  test("ErrorVellumVariable snapshot", async () => {
    const errorVar = codegen.vellumVariable({
      variable: { id: "1", name: "test", type: "ERROR" },
    });
    errorVar.write(writer);
    expect(await writer.toStringFormatted()).toMatchSnapshot();
  });

  test("ArrayVellumVariable snapshot", async () => {
    const arrayVar = codegen.vellumVariable({
      variable: { id: "1", name: "test", type: "ARRAY" },
    });
    arrayVar.write(writer);
    expect(await writer.toStringFormatted()).toMatchSnapshot();
  });

  test("ChatHistoryVellumVariable snapshot", async () => {
    const chatHistoryVar = codegen.vellumVariable({
      variable: { id: "1", name: "test", type: "CHAT_HISTORY" },
    });
    chatHistoryVar.write(writer);
    expect(await writer.toStringFormatted()).toMatchSnapshot();
  });

  test("SearchResultsVellumVariable snapshot", async () => {
    const searchResultsVar = codegen.vellumVariable({
      variable: { id: "1", name: "test", type: "SEARCH_RESULTS" },
    });
    searchResultsVar.write(writer);
    expect(await writer.toStringFormatted()).toMatchSnapshot();
  });

  test("NullVellumVariable snapshot", async () => {
    const nullVar = codegen.vellumVariable({
      variable: { id: "1", name: "test", type: "NULL" },
    });
    nullVar.write(writer);
    expect(await writer.toStringFormatted()).toMatchSnapshot();
  });
});
