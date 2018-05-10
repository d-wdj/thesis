// OPEN BLUE, split and discard channels.
open("/Users/dmtr13/Google Drive/TMTLM/Year 2/Thesis/Cell Lab/NES/ICC_AstraAb/hAstro_P5_A10_1_b.tif");
run("Split Channels");
selectWindow("hAstro_P5_A10_1_b.tif (green)");
close();
selectWindow("hAstro_P5_A10_1_b.tif (red)");
close();

// OPEN GREEN, split and discard channels.
open("/Users/dmtr13/Google Drive/TMTLM/Year 2/Thesis/Cell Lab/NES/ICC_AstraAb/hAstro_P5_A10_1_g.tif");
selectWindow("hAstro_P5_A10_1_g.tif");
run("Split Channels");
selectWindow("hAstro_P5_A10_1_g.tif (blue)");
close();
selectWindow("hAstro_P5_A10_1_g.tif (red)");
close();
selectWindow("hAstro_P5_A10_1_g.tif (green)");
//run("Brightness/Contrast...");
run("Enhance Contrast", "saturated=0.35");


// OPEN RED, split and discard channels.
open("/Users/dmtr13/Google Drive/TMTLM/Year 2/Thesis/Cell Lab/NES/ICC_AstraAb/hAstro_P5_A10_1_r.tif");
selectWindow("hAstro_P5_A10_1_r.tif");
run("Split Channels");
selectWindow("hAstro_P5_A10_1_r.tif (blue)");
close();
selectWindow("hAstro_P5_A10_1_r.tif (green)");
close();


run("Merge Channels...", "c1=[hAstro_P5_A10_1_r.tif (red)] c2=[hAstro_P5_A10_1_g.tif (green)] c3=[hAstro_P5_A10_1_b.tif (blue)] create keep");
run("Stack to RGB");
//saveAs("Tiff", "/Users/dmtr13/Google Drive/TMTLM/Year 2/Thesis/Cell Lab/NES/Try3/ICC_20180405/NORM/LD+_C1.tif");
