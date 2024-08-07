import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  Box,
  Button,
  Heading,
  VStack,
  Text,
  Select,
  Checkbox,
  Input,
  Grid,
  GridItem,
  Popover,
  PopoverTrigger,
  PopoverContent,
  PopoverArrow,
  PopoverCloseButton,
  PopoverHeader,
  PopoverBody,
  IconButton,
  useToast,
} from "@chakra-ui/react";
import { InfoIcon } from "@chakra-ui/icons";
import Breadcrumbs from "./Breadcrumbs";

const Settings = () => {
  // Default values for the settings
  const defaultSettings = {
    motion_sensitivity: "medium",
    object_detection_model: "efficientdet_lite1",
    camera_resolution: "800x600",
    camera_fps: "10",
    recording_length: "5",
    notifications_active: false,
    mailjet_api_key: "",
    mailjet_secret_key: "",
  };

  // State to manage settings
  const [settings, setSettings] = useState(defaultSettings);

  const toast = useToast();

  // Fetch settings on component mount
  useEffect(() => {
    axios
      .get("/api/v1/settings")
      .then((response) => {
        // Assuming the API returns an object with the settings
        setSettings(response.data);
      })
      .catch((error) => console.error("Error fetching settings: ", error));
  }, []);

  const breadcrumbItems = [
    { href: "/", label: "Home" },
    { href: "/settings", label: "Settings", isCurrentPage: true },
  ];

  // Function to reset settings to default values
  const handleReset = () => {
    setSettings(defaultSettings);
  };

  // Function to save current settings
  const handleSave = () => {
    axios
      .put("/api/v1/settings", settings)
      .then((response) => {
        toast({
          title: "Settings saved",
          description: "Your settings have been saved successfully.",
          status: "success",
          duration: 2000,
          isClosable: true,
        });
      })
      .catch((error) => {
        console.error("Error saving settings: ", error);
        toast({
          title: "Error saving settings",
          description: "An error occurred while saving your settings.",
          status: "error",
          duration: 2000,
          isClosable: true,
        });
      });
  };

  return (
    <Box p={5} maxW="800px" mx="auto">
      <Breadcrumbs items={breadcrumbItems} />
      <Box mt={8} p={5} shadow="md" borderWidth="1px" borderRadius="md">
        <Heading size="lg" color="teal.700" mb={4}>
          Settings
        </Heading>
        <VStack align="start" spacing={6} width="100%">
          {/* Motion Detection Sensitivity */}
          <Grid templateColumns="250px 40px 1fr" gap={4} alignItems="center">
            <GridItem>
              <Text fontWeight="bold">Motion Detection Sensitivity</Text>
            </GridItem>
            <GridItem>
              <Popover>
                <PopoverTrigger>
                  <IconButton aria-label="Info" icon={<InfoIcon />} variant="ghost" size="sm" />
                </PopoverTrigger>
                <PopoverContent>
                  <PopoverArrow />
                  <PopoverCloseButton />
                  <PopoverHeader>Motion Detection Sensitivity</PopoverHeader>
                  <PopoverBody>
                    Adjust the sensitivity level for motion detection. Higher sensitivity may detect smaller movements.
                  </PopoverBody>
                </PopoverContent>
              </Popover>
            </GridItem>
            <GridItem>
              <Select
                value={settings.motion_sensitivity}
                onChange={(e) => setSettings({ ...settings, motion_sensitivity: e.target.value })}
                placeholder="Select sensitivity"
                borderColor="gray.400"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
              </Select>
            </GridItem>
          </Grid>

          {/* Object Detection Model Type */}
          <Grid templateColumns="250px 40px 1fr" gap={4} alignItems="center">
            <GridItem>
              <Text fontWeight="bold">Object Detection Model Type</Text>
            </GridItem>
            <GridItem>
              <Popover>
                <PopoverTrigger>
                  <IconButton aria-label="Info" icon={<InfoIcon />} variant="ghost" size="sm" />
                </PopoverTrigger>
                <PopoverContent>
                  <PopoverArrow />
                  <PopoverCloseButton />
                  <PopoverHeader>Object Detection Model Type</PopoverHeader>
                  <PopoverBody>
                    Choose the model type for object detection. Different models offer various levels of accuracy and
                    speed.
                  </PopoverBody>
                </PopoverContent>
              </Popover>
            </GridItem>
            <GridItem>
              <Select
                value={settings.object_detection_model}
                onChange={(e) => setSettings({ ...settings, object_detection_model: e.target.value })}
                placeholder="Select model"
                borderColor="gray.400"
              >
                <option value="efficientdet-lite1">EfficientDet Lite 1</option>
                <option value="efficientdet-lite2">EfficientDet Lite 2</option>
                <option value="efficientdet-lite3">EfficientDet Lite 3</option>
                <option value="efficientdet-lite4">EfficientDet Lite 4</option>
                <option value="ssd-mobilenet-v1">SSD MobileNet v1</option>
                <option value="yolov5-small">YOLOv5 Small</option>
                <option value="yolov5-nano">YOLOv5 Nano</option>
              </Select>
            </GridItem>
          </Grid>

          {/* Camera Resolution */}
          <Grid templateColumns="250px 40px 1fr" gap={4} alignItems="center">
            <GridItem>
              <Text fontWeight="bold">Camera Resolution</Text>
            </GridItem>
            <GridItem>
              <Popover>
                <PopoverTrigger>
                  <IconButton aria-label="Info" icon={<InfoIcon />} variant="ghost" size="sm" />
                </PopoverTrigger>
                <PopoverContent>
                  <PopoverArrow />
                  <PopoverCloseButton />
                  <PopoverHeader>Camera Resolution</PopoverHeader>
                  <PopoverBody>
                    Select the camera resolution for video capture. Higher resolutions provide better quality but may
                    impact performance.
                  </PopoverBody>
                </PopoverContent>
              </Popover>
            </GridItem>
            <GridItem>
              <Select
                value={settings.camera_resolution}
                onChange={(e) => setSettings({ ...settings, camera_resolution: e.target.value })}
                placeholder="Select resolution"
                borderColor="gray.400"
              >
                <option value="640x480">640x480</option>
                <option value="800x600">800x600</option>
                <option value="1024x768">1024x768</option>
                <option value="1280x720">1280x720</option>
              </Select>
            </GridItem>
          </Grid>

          {/* Camera FPS */}
          <Grid templateColumns="250px 40px 1fr" gap={4} alignItems="center">
            <GridItem>
              <Text fontWeight="bold">Camera FPS</Text>
            </GridItem>
            <GridItem>
              <Popover>
                <PopoverTrigger>
                  <IconButton aria-label="Info" icon={<InfoIcon />} variant="ghost" size="sm" />
                </PopoverTrigger>
                <PopoverContent>
                  <PopoverArrow />
                  <PopoverCloseButton />
                  <PopoverHeader>Camera FPS</PopoverHeader>
                  <PopoverBody>
                    Set the frames per second (FPS) for video capture. Higher FPS offers smoother video but may increase
                    resource usage.
                  </PopoverBody>
                </PopoverContent>
              </Popover>
            </GridItem>
            <GridItem>
              <Select
                value={settings.camera_fps}
                onChange={(e) => setSettings({ ...settings, camera_fps: e.target.value })}
                placeholder="Select FPS"
                borderColor="gray.400"
              >
                <option value="5">5</option>
                <option value="10">10</option>
                <option value="15">15</option>
                <option value="20">20</option>
              </Select>
            </GridItem>
          </Grid>

          {/* Recording Length */}
          <Grid templateColumns="250px 40px 1fr" gap={4} alignItems="center">
            <GridItem>
              <Text fontWeight="bold">Recording Length</Text>
            </GridItem>
            <GridItem>
              <Popover>
                <PopoverTrigger>
                  <IconButton aria-label="Info" icon={<InfoIcon />} variant="ghost" size="sm" />
                </PopoverTrigger>
                <PopoverContent>
                  <PopoverArrow />
                  <PopoverCloseButton />
                  <PopoverHeader>Recording Length</PopoverHeader>
                  <PopoverBody>
                    Specify the duration for video recordings in seconds. Longer recording length will result in delayed
                    notification delivery.
                  </PopoverBody>
                </PopoverContent>
              </Popover>
            </GridItem>
            <GridItem>
              <Select
                value={settings.recording_length}
                onChange={(e) => setSettings({ ...settings, recording_length: e.target.value })}
                placeholder="Select length (s)"
                borderColor="gray.400"
              >
                <option value="5">5 seconds</option>
                <option value="10">10 seconds</option>
                <option value="15">15 seconds</option>
                <option value="20">20 seconds</option>
              </Select>
            </GridItem>
          </Grid>

          {/* Notifications Active */}
          <Grid templateColumns="250px 40px 1fr" gap={4} alignItems="center">
            <GridItem>
              <Text fontWeight="bold">Notifications Active</Text>
            </GridItem>
            <GridItem>
              <Popover>
                <PopoverTrigger>
                  <IconButton aria-label="Info" icon={<InfoIcon />} variant="ghost" size="sm" />
                </PopoverTrigger>
                <PopoverContent>
                  <PopoverArrow />
                  <PopoverCloseButton />
                  <PopoverHeader>Notifications Active</PopoverHeader>
                  <PopoverBody>Toggle to enable or disable notifications.</PopoverBody>
                </PopoverContent>
              </Popover>
            </GridItem>
            <GridItem>
              <Checkbox
                isChecked={settings.notifications_active}
                onChange={(e) => setSettings({ ...settings, notifications_active: e.target.checked })}
                borderColor="gray.400"
              />
            </GridItem>
          </Grid>

          {/* Notifications Mailjet API Key */}
          <Grid templateColumns="250px 40px 1fr" gap={4} alignItems="center">
            <GridItem>
              <Text fontWeight="bold">Notifications Mailjet API Key</Text>
            </GridItem>
            <GridItem>
              <Popover>
                <PopoverTrigger>
                  <IconButton aria-label="Info" icon={<InfoIcon />} variant="ghost" size="sm" />
                </PopoverTrigger>
                <PopoverContent>
                  <PopoverArrow />
                  <PopoverCloseButton />
                  <PopoverHeader>Mailjet API Key</PopoverHeader>
                  <PopoverBody>Enter your Mailjet API key for sending notifications.</PopoverBody>
                </PopoverContent>
              </Popover>
            </GridItem>
            <GridItem>
              <Input
                value={settings.mailjet_api_key}
                onChange={(e) => setSettings({ ...settings, mailjet_api_key: e.target.value })}
                placeholder="Enter your Mailjet API key"
                borderColor="gray.400"
              />
            </GridItem>
          </Grid>

          {/* Notifications Mailjet Secret Key */}
          <Grid templateColumns="250px 40px 1fr" gap={4} alignItems="center">
            <GridItem>
              <Text fontWeight="bold">Notifications Mailjet Secret Key</Text>
            </GridItem>
            <GridItem>
              <Popover>
                <PopoverTrigger>
                  <IconButton aria-label="Info" icon={<InfoIcon />} variant="ghost" size="sm" />
                </PopoverTrigger>
                <PopoverContent>
                  <PopoverArrow />
                  <PopoverCloseButton />
                  <PopoverHeader>Mailjet Secret Key</PopoverHeader>
                  <PopoverBody>Enter your Mailjet Secret key for secure communication.</PopoverBody>
                </PopoverContent>
              </Popover>
            </GridItem>
            <GridItem>
              <Input
                value={settings.mailjet_secret_key}
                onChange={(e) => setSettings({ ...settings, mailjet_secret_key: e.target.value })}
                placeholder="Enter your Mailjet Secret key"
                borderColor="gray.400"
              />
            </GridItem>
          </Grid>

          {/* Buttons for Reset and Save */}
          <Grid templateColumns="160px 160px" gap={4} width="100%" mt={6} justifyContent="flex-end">
            <Button onClick={handleReset} colorScheme="red">
              Reset to Defaults
            </Button>
            <Button onClick={handleSave} colorScheme="teal">
              Save
            </Button>
          </Grid>
        </VStack>
      </Box>
    </Box>
  );
};

export default Settings;
